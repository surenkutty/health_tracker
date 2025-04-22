from django.contrib import admin
from .models import Category, Food, FoodLog, Routine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'calories']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'food', 'meal_type', 'date', 'quantity']
    list_filter = ['meal_type', 'date']
    search_fields = ['user__username', 'food__name']


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_completed', 'date']
    list_filter = ['is_completed', 'date']
    search_fields = ['user__username', 'title']
