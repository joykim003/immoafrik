from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'created_at', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone', 'address', 'avatar', 'created_at'),
        }),
    )
    readonly_fields = ('created_at',)
