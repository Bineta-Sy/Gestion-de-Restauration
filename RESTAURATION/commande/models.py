from django.db import models

# Create your models here.
from django.db import models
from menue.models import Plat
from users.models import Client

class Commande(models.Model):
    
    STATUS_CHOICES = [
        ('En cours', 'En cours'),
        ('Prête', 'Prête'),
        ('Servie', 'Servie'),
        ('Annulée', 'Annulée'),
        ('Livrée', 'Livrée'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='En cours')

    TYPE_CHOICES = [
        ('Sur place', 'Sur place'),
        ('À emporter', 'À emporter'),
        ('Livraison', 'Livraison'),
    ]
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE, null=True,blank=True)
    type_commande = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Sur place')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    instruction = models.TextField(default='', blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    est_validee = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"Commande de {self.client.nom} - {self.date_commande.date()}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)


from django.db import models
from menue.models import Plat

class PanierItem(models.Model):
    session_id = models.CharField(max_length=255)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.plat.nom}"
    
