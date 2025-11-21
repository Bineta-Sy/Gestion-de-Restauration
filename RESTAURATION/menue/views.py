from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import Categorie
def liste_plats(request):
    query = request.GET.get('q', '').strip()
    categories = Categorie.objects.prefetch_related('plats').all()

    # On filtre les plats par catégorie
    for cat in categories:
        if query:
            cat.filtered_plats = cat.plats.filter(nom__icontains=query)
        else:
            cat.filtered_plats = cat.plats.all()

    return render(request, 'menue/liste_plats.html', {
        'categories': categories,
        'query': query
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorie
from .forms import CategorieForm
from django.views.decorators.http import require_POST

def liste_categories(request):
    categories = Categorie.objects.all()
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menue:liste_categories')
    else:
        form = CategorieForm()

    return render(request, 'menue/categorie_list.html', {
        'categories': categories,
        'form': form
    })

from django.shortcuts import render, redirect
from .forms import CategorieForm, PlatForm

def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menue:liste_categories')  
    else:
        form = CategorieForm()
    return render(request, 'menue/ajouter_categorie.html', {'form': form})

def ajouter_plat(request):
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menue:ajouter_plat')  
    else:
        form = PlatForm()
    return render(request, 'menue/ajouter_plat.html', {'form': form})


@require_POST
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    categorie.delete()
    return redirect('menue:liste_categories')
