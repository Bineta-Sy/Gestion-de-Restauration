from django.db import models
from commande.models import Commande
from django.utils import timezone

class Facture(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 👈 ajoute default si besoin
    date_emission = models.DateTimeField(default=timezone.now)
    payee = models.BooleanField(default=False)

    def __str__(self):
        return f"Facture #{self.id} - {self.commande.client}"
