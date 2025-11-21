from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Commande, LigneCommande

admin.site.register(Commande)
admin.site.register(LigneCommande)
