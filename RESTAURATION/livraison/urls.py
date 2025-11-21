from django.urls import path
from . import views
app_name = 'livraison'
urlpatterns = [
    path('base/', views.base, name='base'),  
    path('livraisons/', views.LivraisonListView.as_view(), name='livraison_list'),
    path('livraisons/<int:pk>/', views.LivraisonDetailView.as_view(), name='livraison_detail'),
    path('livraisons/creer/', views.LivraisonCreateView.as_view(), name='livraison_create'),
    path('livraisons/<int:pk>/modifier/', views.LivraisonUpdateView.as_view(), name='livraison_update'),
    path('livraisons/<int:pk>/supprimer/', views.LivraisonDeleteView.as_view(), name='livraison_delete'),
    path('livraisons/<int:pk>/changer-statut/<str:new_status>/', views.changer_statut_livraison, name='livraison_changer_statut'),
    path('livraisons/<int:pk>/suivre/', views.suivre_livraison, name='livraison_suivre'),
    path('livraison/<int:livraison_id>/livree/', views.marquer_livree, name='marquer_livree'),
    path('livraisons/<int:pk>/suivi/', views.LivraisonSuiviView.as_view(), name='livraison_suivi'),
    path('suivi/<int:pk>/', views.suivi_livraison, name='suivi_livraison'),
    path('client/voir_livreur/<int:livreur_id>/', views.position_livreur_view, name='position_livreur'),




]