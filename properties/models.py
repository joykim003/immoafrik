from django.db import models
from django.conf import settings
from django.urls import reverse
from users.models import User

DEFAULT_ADMIN_EMAIL = "aflikimmo@mail.com"

class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'Maison'),
        ('apartment', 'Appartement'),
        ('land', 'Terrain'),
    ]

    SELLER_TYPES = [
        ('owner', 'Propriétaire'),
        ('agent', 'Agent immobilier'),
        ('developer', 'Promoteur'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name="Vendeur/Bailleur",
        null=True,  # Temporairement
        blank=True  # Temporairement
    )
    seller_type = models.CharField(
        max_length=20,
        choices=SELLER_TYPES,
        default='owner',
        verbose_name="Type de vendeur"
    )
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    area = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Surface en m²",
        default=0
    )
    image = models.ImageField(upload_to='properties/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'pk': self.pk})

    def get_seller_contact(self):
        """Retourne les informations de contact du vendeur"""
        return {
            'name': self.seller.get_full_name() or self.seller.username,
            'email': self.seller.email,
            'phone': self.seller.phone if hasattr(self.seller, 'phone') else None
        }

    def get_contact_email(self):
        """Retourne l'email de contact pour la propriété"""
        return self.seller.email if self.seller else DEFAULT_ADMIN_EMAIL

    def get_contact_info(self):
        """Retourne les informations de contact"""
        if self.seller:
            return {
                'name': self.seller.get_full_name() or self.seller.username,
                'email': self.seller.email,
                'phone': getattr(self.seller, 'phone', None),
                'whatsapp': getattr(self.seller, 'whatsapp', None),
                'messenger': getattr(self.seller, 'messenger', None),
                'is_admin': False
            }
        return {
            'name': 'AflikImmo',
            'email': DEFAULT_ADMIN_EMAIL,
            'phone': None,
            'whatsapp': None,
            'messenger': None,
            'is_admin': True
        }

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.property.title} du {self.start_date} au {self.end_date}"

class PropertySearch(models.Model):
    PROPERTY_TYPES = [
        ('house', 'Maison'),
        ('apartment', 'Appartement'),
        ('land', 'Terrain'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class PropertyMessage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message de {self.sender} à {self.recipient} - {self.subject}"
