from django.db import models
from commande.models import Commande
from users.models import Livreur

class Livraison(models.Model):
    id = models.AutoField(primary_key=True)
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='livraison')
    status_livraison = models.CharField(max_length=50, default='En préparation') # e.g., 'En préparation', 'En route', 'Livrée'
    position_dps = models.CharField(max_length=255, blank=True, null=True) # Chaîne de position GPS
    livreur = models.ForeignKey(Livreur, on_delete=models.SET_NULL, null=True, blank=True, related_name='livraisons')

    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"

    def __str__(self):
        return f"Livraison {self.id} - {self.status_livraison}"