from django import forms
from .models import Commande

class TypeCommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['type_commande', 'instruction']
        widgets = {
            'type_commande': forms.Select(attrs={'class': 'form-control'}),
            'instruction': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: pas de piment, livrer à 20h...'}),
        }
        labels = {
            'type_commande': 'Choisissez le type de commande :',
            'instruction': 'Instructions supplémentaires (facultatif) :',
        }


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'  
