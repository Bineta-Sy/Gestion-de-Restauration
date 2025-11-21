# from django import forms
# from .models import Table, Reservation

# class TableForm(forms.ModelForm):
#     class Meta:
#         model = Table
#         fields = '__all__'
#         widgets = {
#             'status': forms.Select(choices=[
#                 ('Disponible', 'Disponible'),
#                 ('Occupée', 'Occupée'),
#                 ('Réservée', 'Réservée')
#             ])
#         }

from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'email', 'telephone', 'date', 'heure', 'type_table', 'nombre_personnes', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
        }
