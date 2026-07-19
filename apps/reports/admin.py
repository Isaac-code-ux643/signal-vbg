from django.contrib import admin
from .models import Report, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'vbg_type', 'status', 'urgency', 'created_at']
    list_filter = ['status', 'vbg_type', 'urgency', 'is_anonymous']
    search_fields = ['tracking_code', 'title', 'description']
    readonly_fields = ['tracking_code', 'report_id', 'created_at', 'updated_at', 'ip_address']
    inlines = [AttachmentInline]
    list_per_page = 25

    fieldsets = (
        ('Identifiant', {'fields': ('tracking_code', 'report_id')}),
        ('Signalement', {'fields': ('vbg_type', 'title', 'description', 'date_of_incident')}),
        ('Localisation', {'fields': ('location_description', 'latitude', 'longitude')}),
        ('Statut', {'fields': ('status', 'urgency', 'reporter', 'is_anonymous')}),
        ('Contact', {'fields': ('contact_name', 'contact_phone', 'contact_email'), 'classes': ('collapse',)}),
        ('Métadonnées', {'fields': ('created_at', 'updated_at', 'ip_address'), 'classes': ('collapse',)}),
    )


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'file_type', 'file_size', 'report', 'uploaded_at']
    list_filter = ['file_type']
