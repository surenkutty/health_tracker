from django.db import models
from django.contrib.auth.models import AbstractUser

class ConstomUser(AbstractUser):
    email= models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    address = models.TextField()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone']

    def __str__(self):
        return self.username
    

class UserHealth(models.Model):
    user = models.OneToOneField(ConstomUser, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    daily_calorie_limit = models.PositiveIntegerField(default=2000)


    def __str__(self):
        return f"{self.user.username}'s details"

    

