from django import forms
from .models import Categorie, Plat

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
        }

class PlatForm(forms.ModelForm):
    class Meta:
        model = Plat
        fields = ['nom', 'description', 'prix_Unitaire', 'image', 'categorie']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du plat'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description du plat'}),
            'prix_Unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
        }
