from django.shortcuts import render

from django.http import HttpResponse



from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Livraison
from .forms import LivraisonForm
from commande.models import Commande # Pour lier la livraison à une commande
from users.models import Livreur # Pour assigner un livreur
def base(request):
    return render(request,'livraison/base.html')
# Vues pour Livraison
class LivraisonListView(ListView):
    model = Livraison
    template_name = 'livraison/livraison_list.html'

class LivraisonDetailView(DetailView):
    model = Livraison
    template_name = 'livraison/livraison_detail.html'

class LivraisonCreateView(CreateView):
    model = Livraison
    form_class = LivraisonForm
    template_name = 'livraison/livraison_form.html'
    success_url = reverse_lazy('livraison:livraison_list')

    # Exemple : Assignation automatique du livreur ou de la commande si besoin
    def form_valid(self, form):
        # Vous pourriez vouloir assigner un livreur ici ou récupérer la commande du contexte
        # form.instance.livreur = request.user.livreur (si l'utilisateur connecté est un livreur)
        return super().form_valid(form)

class LivraisonUpdateView(UpdateView):
    model = Livraison
    form_class = LivraisonForm
    template_name = 'livraison/livraison_form.html'
    success_url = reverse_lazy('livraison:livraison_list')

class LivraisonDeleteView(DeleteView):
    model = Livraison
    template_name = 'livraison/livraison_confirm_delete.html'
    success_url = reverse_lazy('livraison:livraison_list')

# Fonction pour mettre à jour le statut de livraison
def changer_statut_livraison(request, pk, new_status):
    livraison = get_object_or_404(Livraison, pk=pk)
    livraison.status_livraison = new_status
    livraison.save()
    return redirect('livraison:livraison_detail', pk=livraison.pk)

# Fonction pour suivre la livraison (pourrait impliquer une API externe)
def suivre_livraison(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    context = {'livraison': livraison, 'position_actuelle': livraison.position_dps}
    return render(request, 'livraison/suivi_livraison.html', context)

#marquer come livrer
def marquer_livree(request, livraison_id):
    livraison = get_object_or_404(Livraison, pk=livraison_id)
    if request.method == 'POST':
        livraison.status_livraison = 'Livrée'
        livraison.save()
        return redirect('users:livreur_dashboard')  # adapte le nom de la route si besoin
    return redirect('users:livreur_dashboard')

from django.views.generic import DetailView
from .models import Livraison

class LivraisonSuiviView(DetailView):
    model = Livraison
    template_name = 'livraison/suivi_livraison.html'

from django.shortcuts import render, get_object_or_404
from .models import Livraison

def suivi_livraison(request, pk):
    livraison = get_object_or_404(Livraison, pk=pk)
    return render(request, 'livraison/suivi_livraison.html', {'livraison': livraison})
from django.shortcuts import render, get_object_or_404

from users.models import Livreur

def position_livreur_view(request, livreur_id):
    livreur = get_object_or_404(Livreur, id=livreur_id)
    return render(request, 'users/position_livreur.html', {'livreur': livreur})

