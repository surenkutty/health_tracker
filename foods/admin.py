from django.contrib import admin
from .models import Category, Food, FoodLog, Routine

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
<<<<<<< HEAD
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

=======
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
>>>>>>> 15348a913ea121b89886f8a7199d8f907394e6f9

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'protein', 'carbs', 'fats')
    list_filter = ('category',)
    search_fields = ('name',)
<<<<<<< HEAD
    autocomplete_fields = ['category']

=======
    autocomplete_fields = ('category',)
>>>>>>> 15348a913ea121b89886f8a7199d8f907394e6f9

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'meal_type', 'date', 'quantity')
<<<<<<< HEAD
    list_filter = ('meal_type', 'date', 'user')
    search_fields = ('food__name', 'user__username')
    autocomplete_fields = ['user', 'food']

=======
    list_filter = ('meal_type', 'date')
    search_fields = ('user__username', 'food__name')
    autocomplete_fields = ('user', 'food')
>>>>>>> 15348a913ea121b89886f8a7199d8f907394e6f9

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'is_completed')
<<<<<<< HEAD
    list_filter = ('date', 'is_completed')
    search_fields = ('title', 'user__username')
    autocomplete_fields = ['user']
=======
    list_filter = ('is_completed', 'date')
    search_fields = ('user__username', 'title')
    autocomplete_fields = ('user',)
>>>>>>> 15348a913ea121b89886f8a7199d8f907394e6f9
