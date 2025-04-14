from django.contrib import admin
from .models import Property
from .models import Reservation

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'location', 'created_at')
    list_filter = ('property_type', 'created_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'description', 'property_type', 'price')
        }),
        ('Localisation', {
            'fields': ('location',)
        }),
        ('Média', {
            'fields': ('image',)
        }),
    )
    
    readonly_fields = ('created_at',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date')
