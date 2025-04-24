from rest_framework import viewsets, permissions
from .models import Category, Food, FoodLog, Routine
from .serializers import CategorySerializer, FoodSerializer, FoodLogSerializer, RoutineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config
import requests
import openai
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]


class FoodLogViewSet(viewsets.ModelViewSet):
    serializer_class = FoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RoutineViewSet(viewsets.ModelViewSet):
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Routine.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

API_KEY="sk-71d91bc1e04749d2866dca3729e5a750"

class AIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user's input and user info
        message = request.data.get('message', '')
        user = request.user

        # Create a custom prompt for the AI
        prompt = f"The user {user.username} asked: {message}. Provide a helpful and healthy food suggestion or tip."

        # Prepare headers with your DeepSeek API Key
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Prepare request data for DeepSeek API
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            # Make the POST request to DeepSeek
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            result = response.json()
            print("DeepSeek Response:", result)

            # Extract AI's response from DeepSeek
            reply = result['choices'][0]['message']['content']
        except Exception as e:
            

            print("DeepSeek API Error:", e)  # Optional: print the error for debugging
            reply = "Sorry, I couldn't generate a reply. Please try again."

        return Response({"reply": reply})


