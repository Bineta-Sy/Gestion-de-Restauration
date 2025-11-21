from django.urls import path
from . import views

app_name = 'commande'
urlpatterns = [
    path('ajouter/<int:plat_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.voir_panier, name='voir_panier'),
path('supprimer_panier/<int:plat_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
     path('panier/valider/', views.valider_panier, name='valider_panier'),
    path('commande/type_commande/<int:commande_id>/', views.type_commande, name='type_commande'),
    path('liste/', views.liste_commandes, name='liste_commandes'),
    path('statistiques/', views.statistiques_commandes, name='statistiques_commandes'),
    path('details/<int:commande_id>/', views.details_commande, name='details_commande'),
    path('supprimer/<int:commande_id>/', views.supprimer_commande, name='supprimer_commande'),
    path('modifier/<int:commande_id>/', views.modifier_commande, name='modifier_commande'),
    path('supprimer_commande_client/<int:commande_id>/', views.supprimer_commande_client, name='supprimer_commande_client'),


]
