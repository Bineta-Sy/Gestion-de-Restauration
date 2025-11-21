from django.urls import path
from . import views

app_name = 'facturation'
urlpatterns = [
    path('base/', views.base, name='base'),
    path('facture/pdf/<int:facture_id>/', views.telecharger_facture, name='telecharger_facture'),
    path('paiement/<int:commande_id>/', views.paiement_qr, name='paiement_qr'),
    path('confirmer_paiement/', views.confirmer_paiement, name='confirmer_paiement'),
]