from django.db import models

# Create your models here.
from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_Unitaire = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='plats/', null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='plats')
    est_epuise = models.BooleanField(default=False) 


    def __str__(self):
        return f"{self.nom} ({self.categorie.nom})"
