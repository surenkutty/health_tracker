from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FoodViewSet, FoodLogViewSet, RoutineViewSet,AIChatView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'foods', FoodViewSet, basename='food')
router.register(r'logs', FoodLogViewSet, basename='foodlog')
router.register(r'routines', RoutineViewSet, basename='routine')

urlpatterns = [
    path('', include(router.urls)),
    path('ai/chat/', AIChatView.as_view(), name='ai-chat'),
]
