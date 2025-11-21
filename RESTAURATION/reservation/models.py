from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from datetime import timedelta

class Reservation(models.Model):
    nom = models.CharField(max_length=100, default='inconnu')
    email = models.EmailField(default='inconnu@example.com')
    telephone = models.CharField(max_length=20, default='0000000000')
    date = models.DateField()
    heure = models.TimeField(default='12:00')
    type_table = models.CharField(max_length=20, choices=[('VIP', 'VIP'), ('Classique', 'Classique')])
    nombre_personnes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.date} à {self.heure}"

    def clean(self):
        super().clean()
        today = timezone.now().date()
        max_date = today + timedelta(days=60)

        if self.date < today:
            raise ValidationError("Impossible de réserver une date passée.")

        if self.date > max_date:
            raise ValidationError("Les réservations ne peuvent pas dépasser 2 mois à l'avance.")
