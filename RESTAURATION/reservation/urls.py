from django.urls import path
from . import views

app_name='reservation'
urlpatterns = [
    path('base/', views.base, name='base'),
    path('reserver/', views.reserver_table, name='reserver_table'),
    path('liste/', views.liste_reservations, name='liste_reservations'),
    path('detail/<int:reservation_id>/', views.detail_reservation, name='detail_reservation'),
    path('modifier/<int:pk>/', views.modifier_reservation, name='modifier_reservation'),
    path('supprimer/<int:pk>/', views.supprimer_reservation, name='supprimer_reservation'),
    path('confirmation/', views.confirmation, name='confirmation'),

]