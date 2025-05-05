from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView,LoginView,UserProfileView,UserHealthView

router = DefaultRouter()
router.register('register',RegistrationView,basename='register')
router.register('login',LoginView,basename='login')
router.register('user-health',UserHealthView,basename='user-health')



urlpatterns = [
    path('',include(router.urls)),
    path('profile/',UserProfileView.as_view(),name='profile')
 
]