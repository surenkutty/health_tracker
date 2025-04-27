from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FoodViewSet, FoodLogViewSet, RoutineViewSet, AIChatView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('foods', FoodViewSet)
router.register('food-logs', FoodLogViewSet)
router.register('routines', RoutineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ai/chat/', AIChatView.as_view(), name='ai-chat'),
]


    