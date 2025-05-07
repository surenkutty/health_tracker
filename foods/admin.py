from django.contrib import admin
from .models import Category, Food, FoodLog, Routine

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'protein', 'carbs', 'fats')
    list_filter = ('category',)
    search_fields = ('name',)
    autocomplete_fields = ['category']


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'meal_type', 'date', 'quantity')
    list_filter = ('meal_type', 'date', 'user')
    search_fields = ('food__name', 'user__username')
    autocomplete_fields = ['user', 'food']


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'is_completed')
    list_filter = ('date', 'is_completed')
    search_fields = ('title', 'user__username')
    autocomplete_fields = ['user']
