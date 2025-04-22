from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView,LoginView,UserProfileView,UserHealthView

router = DefaultRouter()
router.register('register',RegistrationView,basename='register')
router.register('login',LoginView,basename='login')
router.register('health',UserHealthView,basename='health')
router.register('profile',UserProfileView,basename='profile')


urlpatterns = [
    path('',include(router.urls)),
 
]