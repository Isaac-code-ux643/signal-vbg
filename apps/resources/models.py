from django.db import models


class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'faq_categories'
        ordering = ['order']
        verbose_name = 'Categorie FAQ'
        verbose_name_plural = 'Categories FAQ'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    keywords = models.TextField(help_text="Mots-cles separes par des virgules")
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faqs'
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('guide', 'Guide'),
        ('brochure', 'Brochure'),
        ('video', 'Video'),
        ('link', 'Lien externe'),
        ('phone', "Numero d'urgence"),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    description = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    url = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resources'
        ordering = ['-created_at']
        verbose_name = 'Ressource'
        verbose_name_plural = 'Ressources'

    def __str__(self):
        return self.title
