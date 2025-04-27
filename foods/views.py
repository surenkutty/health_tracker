from rest_framework import viewsets, permissions
from .models import Category, Food, FoodLog, Routine
from .serializers import CategorySerializer, FoodSerializer, FoodLogSerializer, RoutineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config
import requests
import openai
from rest_framework.decorators import action
from django.db.models import Sum, F,Count
from collections import defaultdict
from datetime import datetime,timedelta


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

class FoodLogViewSet(viewsets.ModelViewSet):
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date = request.query_params.get('date')
        if not date:
            date = datetime.today().date()

        logs = FoodLog.objects.filter(user=request.user, date=date)
        summary = logs.aggregate(
            total_calories=Sum(F('quantity') * F('food__calories')),
            total_protein=Sum(F('quantity') * F('food__protein')),
            total_carbs=Sum(F('quantity') * F('food__carbs')),
            total_fats=Sum(F('quantity') * F('food__fats')),
        )
        return Response({key: value or 0 for key, value in summary.items()})

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Show user previous food logs grouped by date"""
        logs = FoodLog.objects.filter(user=request.user).order_by('-date')
        history = defaultdict(list)

        for log in logs:
            history[str(log.date)].append({
                'food_name': log.food.name,
                'quantity': log.quantity,
                'meal_type': log.meal_type,
                'calories': log.food.calories * log.quantity,
                'protein': (log.food.protein or 0) * log.quantity,
                'carbs': (log.food.carbs or 0) * log.quantity,
                'fats': (log.food.fats or 0) * log.quantity,
            })

        return Response(history)
    @action(detail=False, methods=['get'])
    def weekly_summary(self, request):
        """Show last 7 days food summary"""
        today = datetime.today().date()
        last_week = today - timedelta(days=6)  # 6 days back + today = 7 days

        logs = FoodLog.objects.filter(user=request.user, date__range=[last_week, today])

        summary_per_day = defaultdict(lambda: {
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fats': 0
        })

        for log in logs:
            date_str = str(log.date)
            summary_per_day[date_str]['total_calories'] += (log.food.calories * log.quantity)
            summary_per_day[date_str]['total_protein'] += ((log.food.protein or 0) * log.quantity)
            summary_per_day[date_str]['total_carbs'] += ((log.food.carbs or 0) * log.quantity)
            summary_per_day[date_str]['total_fats'] += ((log.food.fats or 0) * log.quantity)

        return Response(summary_per_day)
    @action(detail=False, methods=['get'])
    def top_foods(self, request):
        """Show top eaten foods by user"""
        foods = FoodLog.objects.filter(user=request.user)\
            .values('food__name')\
            .annotate(times_eaten=Count('id'))\
            .order_by('-times_eaten')[:5]  # Top 5 foods

        return Response(foods)
    @action(detail=False, methods=['get'])
    def goal_progress(self, request):
        """Calories goal vs achieved today"""
        today = datetime.today().date()
        logs = FoodLog.objects.filter(user=request.user, date=today)

        total_calories = logs.aggregate(
            total=Sum(F('quantity') * F('food__calories'))
        )['total'] or 0

        user_details = request.user.userdetails  # assuming OneToOne with UserDetails
        daily_goal = user_details.daily_calorie_limit

        percentage = (total_calories / daily_goal) * 100 if daily_goal else 0

        return Response({
            'goal': daily_goal,
            'achieved': total_calories,
            'percentage': round(percentage, 2)
        })







class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

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


