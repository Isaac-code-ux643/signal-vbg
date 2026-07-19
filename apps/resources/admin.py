from django.contrib import admin
from .models import FAQCategory, FAQ, Resource


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 0


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    inlines = [FAQInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_published', 'order']
    list_filter = ['category', 'is_published']
    search_fields = ['question', 'answer', 'keywords']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'is_published', 'created_at']
    list_filter = ['resource_type', 'is_published']
    search_fields = ['title', 'description']
