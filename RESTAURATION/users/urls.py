from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    path('base/', views.base, name='base'), 
    #path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login_django'),
   
    path('utilisateurs/creer/', views.UtilisateurCreateView.as_view(), name='utilisateur_create'),
    path('utilisateurs/', views.UtilisateurListView.as_view(), name='utilisateur_list'),
    path('utilisateurs/<int:pk>/', views.UtilisateurDetailView.as_view(), name='utilisateur_detail'),
    path('utilisateurs/<int:pk>/modifier/', views.UtilisateurUpdateView.as_view(), name='utilisateur_update'),
    path('utilisateurs/<int:pk>/supprimer/', views.UtilisateurDeleteView.as_view(), name='utilisateur_delete'),
    path('clients/creer/', views.ClientCreateView.as_view(), name='client_create'),
    path('connexion/', views.connexion_view, name='login'),
    path('creer_compte/', views.creer_compte_view, name='creer_compte'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   # path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('serveur_dashboard/', views.serveur_dashboard, name='serveur_dashboard'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('cuisinier_dashboard/', views.cuisinier_dashboard, name='cuisinier_dashboard'),
    path('livreur_dashboard/', views.livreur_dashboard, name='livreur_dashboard'),

    #status commande pour le cuisinier
     path(
        'changer_statut_commande/<int:commande_id>/<str:nouveau_statut>/',
        views.changer_statut_commande,
        name='changer_statut_commande'
    ),
        
    path('commande/supprimer/<int:id>/', views.supprimer_commande, name='supprimer_commande'),
    path('messagerie/', views.messagerie_view, name='messagerie'),
    path('maj_position_livreur/', views.maj_position_livreur, name='maj_position_livreur'),
    path('client/voir_livreur/<int:livreur_id>/', views.position_livreur_view, name='position_livreur'),
    path('client/position_json/<int:livreur_id>/', views.position_livreur_json, name='position_livreur_json'),
    path('plat/<int:plat_id>/epuise/', views.marquer_epuise, name='marquer_epuise'),






]
