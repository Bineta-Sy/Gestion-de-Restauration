from django import forms
from .models import Utilisateur, Client, Administrateur, Manager, Cuisinier, Serveur, Livreur
from .models import Message, Utilisateur
from .models import Message


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = '__all__' 
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
            'role': forms.Select(choices=Utilisateur.ROLES),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }

class AdministrateurForm(forms.ModelForm):
    class Meta:
        model = Administrateur
        fields = '__all__'
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }

class CuisinierForm(forms.ModelForm):
    class Meta:
        model = Cuisinier
        fields = '__all__'
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }

class ServeurForm(forms.ModelForm):
    class Meta:
        model = Serveur
        fields = '__all__'
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }

class LivreurForm(forms.ModelForm):
    class Meta:
        model = Livreur
        fields = '__all__'
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }



# forms.py
from django import forms
from .models import Message, Utilisateur

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['destinataire', 'contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Tapez votre message ici...'
            }),
            'destinataire': forms.HiddenInput(),  
        }

    def __init__(self, *args, **kwargs):
        utilisateur = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if utilisateur:
            pass