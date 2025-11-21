from django.urls import path
from .views import liste_plats
from . import views

app_name = 'menue'
urlpatterns = [
    path('', liste_plats, name='liste_plats'),
     path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/supprimer/<int:categorie_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('ajouter_categorie/', views.ajouter_categorie, name='ajouter_categorie'),
    path('ajouter_plat/', views.ajouter_plat, name='ajouter_plat'),
]