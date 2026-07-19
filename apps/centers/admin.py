from django.contrib import admin
from .models import SupportCenter


@admin.register(SupportCenter)
class SupportCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'center_type', 'city', 'province', 'is_active']
    list_filter = ['center_type', 'is_active', 'is_free', 'accepts_anonymous']
    search_fields = ['name', 'city', 'address', 'description']
    list_per_page = 25
