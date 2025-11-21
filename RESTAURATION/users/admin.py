from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Utilisateur, Client, Serveur, Cuisinier, Manager, Administrateur, Livreur

admin.site.register(Utilisateur)
admin.site.register(Client)
admin.site.register(Serveur)
admin.site.register(Cuisinier)
admin.site.register(Manager)
admin.site.register(Administrateur)
admin.site.register(Livreur)
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'contenu', 'lu', 'date_envoi')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('contenu',)
