from django.contrib import admin
from .models import Category, Food, FoodLog, Routine

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'protein', 'carbs', 'fats')
    list_filter = ('category',)
    search_fields = ('name',)
    autocomplete_fields = ('category',)

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'meal_type', 'date', 'quantity')
    list_filter = ('meal_type', 'date')
    search_fields = ('user__username', 'food__name')
    autocomplete_fields = ('user', 'food')

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'is_completed')
    list_filter = ('is_completed', 'date')
    search_fields = ('user__username', 'title')
    autocomplete_fields = ('user',)
