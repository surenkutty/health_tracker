from rest_framework import viewsets, permissions
from .models import Category, Food, FoodLog, Routine
from .serializers import CategorySerializer, FoodSerializer, FoodLogSerializer, RoutineSerializer


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
