from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ConstomUser, UserHealth


class CustomUserAdmin(UserAdmin):
    model = ConstomUser
    list_display = ['id', 'email', 'username', 'phone', 'address', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email', 'username', 'phone']
    ordering = ['id']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone', 'address', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    filter_horizontal = ('groups', 'user_permissions')


@admin.register(UserHealth)
class UserHealthAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'weight', 'daily_calorie_limit']
    search_fields = ['user__username', 'user__email']


admin.site.register(ConstomUser, CustomUserAdmin)

