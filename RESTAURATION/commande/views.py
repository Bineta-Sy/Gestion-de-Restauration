from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from menue.models import Plat



def ajouter_au_panier(request, plat_id):
    panier = request.session.get('panier', {})
    panier[str(plat_id)] = panier.get(str(plat_id), 0) + 1
    request.session['panier'] = panier
    return redirect('commande:voir_panier')
def voir_panier(request):
    panier = request.session.get('panier', {})
    plats = []
    total = 0

    # On parcourt une copie des clés pour éviter l'erreur
    for pid in list(panier.keys()):
        quantite = panier[pid]
        try:
            plat = Plat.objects.get(pk=pid)
            total += plat.prix_Unitaire * quantite
            plats.append({'plat': plat, 'quantite': quantite})
        except Plat.DoesNotExist:
            # Supprime l'ID du panier si le plat n'existe plus
            panier.pop(pid)

    # Mise à jour du panier nettoyé dans la session
    request.session['panier'] = panier

    return render(request, 'commande/panier.html', {'panier': plats, 'total': total})


def supprimer_du_panier(request, plat_id):
    panier = request.session.get('panier', {})
    if str(plat_id) in panier:
        del panier[str(plat_id)]
        request.session['panier'] = panier
    return redirect('commande:voir_panier')
from django.shortcuts import render, redirect
from django.urls import reverse
from commande.models import Plat, Commande, LigneCommande
from users.models import Client

def valider_panier(request):
    if not request.session.get('email') or request.session.get('role') != 'CLIENT':
        return redirect(f"{reverse('users:login')}?next={request.path}")

    panier = request.session.get('panier', {})
    plats = []
    total = 0

    for plat_id, quantite in panier.items():
        try:
            plat = Plat.objects.get(id=plat_id)
            plats.append({
                'plat': plat,
                'quantite': quantite,
                'total': plat.prix_Unitaire * quantite
            })
            total += plat.prix_Unitaire * quantite
        except Plat.DoesNotExist:
            continue

    email = request.session.get('email')
    client = Client.objects.get(email=email)

    commande = Commande.objects.create(client=client, total=total)

    for item in plats:
        LigneCommande.objects.create(
            commande=commande,
            plat=item['plat'],
            quantite=item['quantite']
        )

    # ✅ Vider le panier après validation
    request.session.pop('panier', None)

    # Stocker l'ID de la commande
    request.session['commande_id'] = commande.id

    return redirect('commande:type_commande', commande_id=commande.id)

from django.shortcuts import render, redirect, get_object_or_404
from .forms import TypeCommandeForm
from .models import Commande

def type_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    if request.method == 'POST':
        form = TypeCommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('facturation:paiement_qr', commande_id=commande.id)  
    else:
        form = TypeCommandeForm(instance=commande)

    return render(request, 'commande/type_commande.html', {
        'form': form,
        'commande': commande
    })


def liste_commandes(request):
    commandes = Commande.objects.select_related('client', 'plat')  
    return render(request, 'commande/liste_commandes.html', {
        'commandes': commandes
    })

from django.shortcuts import render, get_object_or_404
from .models import Commande  

def details_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    return render(request, 'commande/details_commande.html', {'commande': commande})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Commande
from .forms import CommandeForm  

def modifier_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('commande:liste_commandes')  
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'commande/modifier_commande.html', {'form': form})
def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.delete()
    return redirect('commande:liste_commandes')

from django.db.models import Count, Sum
from .models import Commande

def statistiques_commandes(request):
    total_commandes = Commande.objects.count()
    quantite_totale = Commande.objects.aggregate(Sum('total'))['total__sum'] or 0

    commandes_par_statut = Commande.objects.values('status').annotate(total=Count('id'))
    commandes_par_type = Commande.objects.values('type_commande').annotate(total=Count('id'))
    commandes_par_date = Commande.objects.extra(select={'date_only': "DATE(date_commande)"}).values('date_only').annotate(total=Count('id'))

    context = {
        'total_commandes': total_commandes,
        'quantite_totale': quantite_totale,
        'commandes_par_statut': commandes_par_statut,
        'commandes_par_type': commandes_par_type,
        'commandes_par_date': commandes_par_date,
    }
    return render(request, 'commande/statistiques_commandes.html', context)

####supprimer commande par client
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from commande.models import Commande

def supprimer_commande_client(request, commande_id):
    if request.method == 'POST':
        try:
            commande = get_object_or_404(Commande, id=commande_id)
            commande.delete()
            messages.success(request, "Commande supprimée avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {e}")
    else:
        messages.error(request, "Méthode non autorisée pour la suppression.")
    return redirect('users:client_dashboard')




