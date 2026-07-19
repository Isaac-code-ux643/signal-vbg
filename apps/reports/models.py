import uuid
import random
import string
from django.db import models
from django.conf import settings


def generate_tracking_code():
    while True:
        code = 'VBG-'
        code += ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        code += '-'
        code += ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if not Report.objects.filter(tracking_code=code).exists():
            return code


class Report(models.Model):
    VBG_TYPES = [
        ('physical', 'Violence physique'),
        ('sexual', 'Violence sexuelle'),
        ('psychological', 'Violence psychologique'),
        ('economic', 'Violence économique'),
        ('domestic', 'Violence domestique'),
        ('other', 'Autre'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Soumis'),
        ('under_review', "En cours d'examen"),
        ('in_progress', 'En cours de traitement'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
        ('rejected', 'Rejeté'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('critical', 'Critique'),
    ]

    tracking_code = models.CharField(max_length=12, unique=True, editable=False)
    report_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reports'
    )
    is_anonymous = models.BooleanField(default=False)

    vbg_type = models.CharField(max_length=20, choices=VBG_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_of_incident = models.DateField()
    location_description = models.CharField(max_length=300, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')

    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'

    def __str__(self):
        return f"[{self.tracking_code}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = generate_tracking_code()
        super().save(*args, **kwargs)


class Attachment(models.Model):
    ATTACHMENT_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('video', 'Vidéo'),
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/')
    file_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    original_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attachments'
        verbose_name = 'Pièce jointe'
        verbose_name_plural = 'Pièces jointes'

    def __str__(self):
        return f"{self.original_name} ({self.report.tracking_code})"
