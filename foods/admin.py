from django.contrib import admin
from .models import Category, Food, FoodLog, Routine
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RelatedDropdownFilter, RangeDateFilter

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Food)
class FoodAdmin(ModelAdmin):
    list_display = ['id', 'name', 'category', 'calories']
    list_filter = [('category', RelatedDropdownFilter)]
    search_fields = ['name']


@admin.register(FoodLog)
class FoodLogAdmin(ModelAdmin):
    list_display = ['id', 'user', 'food', 'meal_type', 'date', 'quantity']
    list_filter = [
        ('meal_type', ChoicesDropdownFilter),
        ('date', RangeDateFilter)
    ]
    search_fields = ['user__username', 'food__name']


@admin.register(Routine)
class RoutineAdmin(ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_completed', 'date']
    list_filter = [
        ('is_completed', ChoicesDropdownFilter),
        ('date', RangeDateFilter)
    ]
    search_fields = ['user__username', 'title']
