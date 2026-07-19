from django.db import models


class SupportCenter(models.Model):
    CENTER_TYPES = [
        ('hospital', 'Hôpital/Clinique'),
        ('police', 'Poste de police'),
        ('ngo', 'ONG'),
        ('social', 'Service social'),
        ('legal', 'Aide juridique'),
        ('psychological', 'Soutien psychologique'),
        ('shelter', "Centre d'hébergement"),
    ]

    name = models.CharField(max_length=200)
    center_type = models.CharField(max_length=20, choices=CENTER_TYPES)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    services_offered = models.TextField(help_text="Liste des services offerts")
    opening_hours = models.CharField(max_length=200)
    is_free = models.BooleanField(default=True)
    accepts_anonymous = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'support_centers'
        ordering = ['name']
        verbose_name = "Centre d'aide"
        verbose_name_plural = "Centres d'aide"

    def __str__(self):
        return f"{self.name} ({self.get_center_type_display()})"
