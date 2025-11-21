from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import Utilisateur, Client, Administrateur, Manager, Cuisinier, Serveur, Livreur
from commande.models import Commande, LigneCommande

from .forms import (
    UtilisateurForm, ClientForm, AdministrateurForm, ManagerForm,
    CuisinierForm, ServeurForm, LivreurForm
)

# Accueil de base
def base(request):
    return render(request, 'users/base.html')

# Accueil général
def home_view(request):
    context = {
        'welcome_message': "Bienvenue sur la page d'accueil de notre restaurant !",
    }
    return render(request, 'home.html', context)

from django.contrib.auth.hashers import check_password
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def connexion_view(request):
    error = None
    next_url = request.GET.get('next', '')  

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            utilisateur = Utilisateur.objects.get(email=email)
            print("Utilisateur trouvé :", utilisateur)

            if check_password(password, utilisateur.mot_de_passe):
                role = utilisateur.role.upper()
                request.session['role'] = role
                request.session['email'] = utilisateur.email 

                print("Mot de passe OK ✅")
                print("Rôle :", role)

                # Vérifie que l'URL est sûre pour éviter les redirections externes
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)

                if role == 'ADMIN':
                    return redirect('users:admin_dashboard')
                elif role == 'SERVEUR':
                    return redirect('users:serveur_dashboard')
                elif role == 'CUISINIER':
                    return redirect('users:cuisinier_dashboard')
                elif role == 'LIVREUR':
                    return redirect('users:livreur_dashboard')
                elif role == 'CLIENT':
                    request.session['panier'] = {}  # Réinitialisation le panier
                    return redirect('users:client_dashboard')
                else:
                    error = "Rôle inconnu"
            else:
                error = " Mot de passe incorrect"
                print(error)
        except Utilisateur.DoesNotExist:
            error = " Aucun utilisateur avec cet email"
            print(error)

    return render(request, 'users/login.html', {'error': error})

# Vue création de compte
def creer_compte_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            # Hash du mot de passe si tu l’implémentes manuellement
            utilisateur.mot_de_passe = make_password(utilisateur.mot_de_passe)
            utilisateur.save()
            messages.success(request, "Compte créé avec succès. Vous pouvez vous connecter.")

            return redirect('users:login')

    else:
        form = ClientForm()
    return render(request, 'users/creer_compte.html', {'form': form})


class UtilisateurListView(ListView):
    model = Utilisateur
    template_name = 'users/utilisateur_list.html'

class UtilisateurDetailView(DetailView):
    model = Utilisateur
    template_name = 'users/utilisateur_detail.html'

class UtilisateurCreateView(CreateView):
    model = Utilisateur
    form_class = UtilisateurForm
    template_name = 'users/utilisateur_form.html'
    success_url = reverse_lazy('users:utilisateur_list')

class UtilisateurUpdateView(UpdateView):
    model = Utilisateur
    form_class = UtilisateurForm
    template_name = 'users/utilisateur_form.html'
    success_url = reverse_lazy('users:utilisateur_list')

class UtilisateurDeleteView(DeleteView):
    model = Utilisateur
    template_name = 'users/utilisateur_confirm_delete.html'
    success_url = reverse_lazy('users:utilisateur_list')

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'users/client_form.html'
    success_url = reverse_lazy('users:client_list')

from django.shortcuts import render, redirect
from django.utils.timezone import now, make_aware
from django.db.models import Sum
from datetime import datetime, timedelta
from commande.models import Commande

def admin_dashboard(request):
    if request.session.get('role') != 'ADMIN':
        return redirect('users:login')

    today = now().date()
    yesterday = today - timedelta(days=1)
    start_of_day = make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = make_aware(datetime.combine(today, datetime.max.time()))
    start_of_yesterday = make_aware(datetime.combine(yesterday, datetime.min.time()))
    end_of_yesterday = make_aware(datetime.combine(yesterday, datetime.max.time()))

    month = today.month
    last_month = month - 1 if month > 1 else 12
    year = today.year
    last_month_year = year - 1 if month == 1 else year

    #  Commandes et revenus aujourd’hui
    commandes_jour = Commande.objects.filter(date_commande__range=(start_of_day, end_of_day)).count()
    revenus_jour = Commande.objects.filter(date_commande__range=(start_of_day, end_of_day)).aggregate(total=Sum('total'))['total'] or 0

    #  Hier
    commandes_hier = Commande.objects.filter(date_commande__range=(start_of_yesterday, end_of_yesterday)).count()
    revenus_hier = Commande.objects.filter(date_commande__range=(start_of_yesterday, end_of_yesterday)).aggregate(total=Sum('total'))['total'] or 0

    #  Ce mois
    commandes_mois = Commande.objects.filter(date_commande__month=month, date_commande__year=year).count()
    revenus_mois = Commande.objects.filter(date_commande__month=month, date_commande__year=year).aggregate(total=Sum('total'))['total'] or 0

    #  Mois dernier
    commandes_mois_prec = Commande.objects.filter(date_commande__month=last_month, date_commande__year=last_month_year).count()
    revenus_mois_prec = Commande.objects.filter(date_commande__month=last_month, date_commande__year=last_month_year).aggregate(total=Sum('total'))['total'] or 0

    #  Cette année
    commandes_annee = Commande.objects.filter(date_commande__year=year).count()
    revenus_annee = Commande.objects.filter(date_commande__year=year).aggregate(total=Sum('total'))['total'] or 0

    #  Pourcentages
    def pourcentage(actuel, precedent):
        if precedent == 0:
            return 100 if actuel > 0 else 0
        return round(((actuel - precedent) / precedent) * 100, 2)

    evolution_commandes_jour = pourcentage(commandes_jour, commandes_hier)
    evolution_revenus_jour = pourcentage(revenus_jour, revenus_hier)
    evolution_commandes_mois = pourcentage(commandes_mois, commandes_mois_prec)
    evolution_revenus_mois = pourcentage(revenus_mois, revenus_mois_prec)

    return render(request, 'users/admin_dashboard.html', {
        'commandes_jour': commandes_jour,
        'revenus_jour': revenus_jour,
        'commandes_mois': commandes_mois,
        'revenus_mois': revenus_mois,
        'commandes_annee': commandes_annee,
        'revenus_annee': revenus_annee,
        'evolution_commandes_jour': evolution_commandes_jour,
        'evolution_revenus_jour': evolution_revenus_jour,
        'evolution_commandes_mois': evolution_commandes_mois,
        'evolution_revenus_mois': evolution_revenus_mois,
        'administrateur': request.user,
    })

from django.shortcuts import render, redirect
from commande.models import Commande

def serveur_dashboard(request):
    if request.session.get('role') != 'SERVEUR':
        return redirect('users:login')

    # Requête pour récupérer commandes prêtes 'Sur place' avec leurs lignes en un minimum de requêtes
    commandes_pretes = Commande.objects.filter(status='Prête', type_commande='Sur place').order_by('-date_commande').prefetch_related('lignecommande_set', 'lignecommande_set__plat')


    return render(request, 'users/serveur_dashboard.html', {
        'commandes_pretes': commandes_pretes
    })


from commande.models import Commande

def cuisinier_dashboard(request):
    if request.session.get('role') != 'CUISINIER':
        return redirect('users:login')

    commandes = Commande.objects.filter(status='En cours').prefetch_related('lignecommande_set__plat')

    return render(request, 'users/cuisinier_dashboard.html', {
        'commandes': commandes
    })


from livraison.models import Livraison

from users.models import Livreur

def livreur_dashboard(request):
    if request.session.get('role') != 'LIVREUR':
        return redirect('users:login')

    email = request.session.get('email')
    if not email:
        return redirect('users:login')

    try:
        livreur = Livreur.objects.get(email=email)
    except Livreur.DoesNotExist:
        return render(request, 'users/livreur_dashboard.html', {
            'error': "Vous n'êtes pas enregistré comme livreur."
        })

    # Récupérer les livraisons du livreur, dont la commande est prête et de type livraison
    livraisons = Livraison.objects.filter(
        commande__status='Prête',
        commande__type_commande='Livraison',
        livreur=livreur
    ).select_related('commande__client')

    return render(request, 'users/livreur_dashboard.html', {
        'livraisons': livraisons,
        'livreur': livreur
    })

from django.shortcuts import render, redirect
from commande.models import Commande
from users.models import Client

from livraison.models import Livraison

def client_dashboard(request):
    if request.session.get('role') != 'CLIENT':
        return redirect('users:login')

    email = request.session.get('email')
    if not email:
        return redirect('users:login')

    try:
        client = Client.objects.get(email=email)
    except Client.DoesNotExist:
        return render(request, 'users/client_dashboard.html', {
            'error': "Vous n'êtes pas enregistré comme client."
        })

    commandes = Commande.objects.filter(client=client).order_by('-date_commande')

    # ➕ Récupérer la livraison en cours pour les commandes "Prête" et "Livraison"
    livraison_active = (
        Livraison.objects
        .filter(
            commande__client=client,
            commande__status='Prête',
            commande__type_commande='Livraison'
        )
        .select_related('livreur')
        .first()
    )

    livreur = livraison_active.livreur if livraison_active else None

    return render(request, 'users/client_dashboard.html', {
        'commandes': commandes,
        'client': client,
        'livreur': livreur,  # ← à envoyer au template
    })


"""" Changer status commande pour cuisisnier"""

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from commande.models import Commande

@require_POST
def changer_statut_commande(request, commande_id, nouveau_statut):
    # Récupérer la commande ou 404 si non trouvée
    commande = get_object_or_404(Commande, id=commande_id)
    # Liste des statuts autorisés (adapter selon ton modèle)
    statuts_valides = ['En cours', 'Prête', 'Servie', 'Annulée']
    if nouveau_statut not in statuts_valides:
        # Tu peux gérer l'erreur ici, par ex. message d'erreur
        return redirect('users:cuisinier_dashboard')
    # Modifier le statut
    commande.status = nouveau_statut
    commande.save()
    # Rediriger vers le dashboard cuisinier
    return redirect('users:cuisinier_dashboard')
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.delete()
    return JsonResponse({'success': True})
#Changer status commande dans server dashboard
from django.urls import reverse


#####systeme chat

"""def test_view(request):
    form = TestForm()
    return render(request, 'users/test_form.html', {'form': form})"""


from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from .models import Utilisateur, Message
from .forms import MessageForm

from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from .models import Utilisateur, Message
from .forms import MessageForm

from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Utilisateur, Message
from .forms import MessageForm

def messagerie_view(request):
    email = request.session.get('email')
    if not email:
        raise Http404("Utilisateur non connecté.")

    try:
        utilisateur = Utilisateur.objects.get(email=email)
    except Utilisateur.DoesNotExist:
        raise Http404("Utilisateur introuvable.")

    # Liste des destinataires (exclut le user courant et clients par exemple)
    destinataires = Utilisateur.objects.exclude(id=utilisateur.id).exclude(role='CLIENT').exclude(role='MANAGER')

    destinataire_id = request.GET.get('destinataire_id')
    destinataire_selectionne = None
    messages_conversation = []

    if destinataire_id:
        try:
            destinataire_selectionne = Utilisateur.objects.get(id=destinataire_id)
            messages_conversation = Message.objects.filter(
                Q(expediteur=utilisateur, destinataire=destinataire_selectionne) |
                Q(expediteur=destinataire_selectionne, destinataire=utilisateur)
            ).order_by('date_envoi')
        except Utilisateur.DoesNotExist:
            destinataire_selectionne = None

    if request.method == 'POST':
        form = MessageForm(request.POST, user=utilisateur)
        if form.is_valid():
            message = form.save(commit=False)
            message.expediteur = utilisateur
            message.save()
            # Redirection vers la même page avec le destinataire sélectionné pour afficher la conversation mise à jour
            return redirect(f"{request.path}?destinataire_id={message.destinataire.id}")
    else:
        # Si on a un destinataire sélectionné, pré-remplir le champ caché destinataire
        initial_data = {'destinataire': destinataire_selectionne.id} if destinataire_selectionne else {}
        form = MessageForm(user=utilisateur, initial=initial_data)

    return render(request, 'users/messagerie.html', {
        'user': utilisateur,
        'destinataires': destinataires,
        'destinataire': destinataire_selectionne,
        'messages': messages_conversation,
        'form': form,
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def maj_position_livreur(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        try:
            livreur = Livreur.objects.get(email=email)
            livreur.latitude = latitude
            livreur.longitude = longitude
            livreur.save()
            return JsonResponse({'success': True})
        except Livreur.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Livreur non trouvé'})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Livreur


from django.shortcuts import render
from users.models import Livreur
from django.http import JsonResponse

def position_livreur_view(request, livreur_id):
    try:
        livreur = Livreur.objects.get(id=livreur_id)
        return render(request, 'users/position_livreur.html', {
            'livreur': livreur
        })
    except Livreur.DoesNotExist:
        return render(request, 'users/position_livreur.html', {
            'error': "Livreur non trouvé"
        })

def position_livreur_json(request, livreur_id):
    try:
        livreur = Livreur.objects.get(id=livreur_id)
        return JsonResponse({
            'latitude': livreur.latitude,
            'longitude': livreur.longitude
        })
    except Livreur.DoesNotExist:
        return JsonResponse({'error': 'Livreur non trouvé'}, status=404)

from menue.models import Plat

def marquer_epuise(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    plat.est_epuise = True
    plat.save()

    commandes = Commande.objects.filter(lignecommande__plat=plat, status='En cours')
    commandes.update(status='Annulée')

    return redirect('users:cuisinier_dashboard')  # Ajuste avec ton nom de vue
