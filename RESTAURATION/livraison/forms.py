from django import forms
from .models import Livraison
from commande.models import Commande  

class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = '__all__'
        widgets = {
            'status_livraison': forms.Select(choices=[ 
                ('En préparation', 'En préparation'),
                ('En route', 'En route'),
                ('Livrée', 'Livrée')
            ]),
            'position_dps': forms.TextInput(attrs={'placeholder': 'Ex: Lat:XX.X, Lon:YY.Y'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['commande'].queryset = Commande.objects.filter(
            type_commande='Livraison',
            status='Prête'
        )
