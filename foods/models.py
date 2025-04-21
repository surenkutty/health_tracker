from django.db import models
from accounts.models import User

MEAL_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('snacks', 'Snacks'),
    ('lunch', 'Lunch'),
    ('tea', 'Tea'),
    ('dinner', 'Dinner'),
]

class FoodItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    calories = models.FloatField()
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    portion_size = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)

    def total_calories(self):
        return self.food_item.calories * self.quantity

class FoodRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    day_of_week = models.CharField(max_length=10)

