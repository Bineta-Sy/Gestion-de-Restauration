from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = '__all__'
        widgets = {
            'montant': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'pdf_url': forms.URLInput(attrs={'readonly': 'readonly'}),
        }

from django import forms

class PaiementForm(forms.Form):
    code_transaction = forms.CharField(label="Code de transaction reçu", max_length=100)
