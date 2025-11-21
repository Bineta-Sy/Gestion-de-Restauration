# from django.shortcuts import render

# from django.http import HttpResponse

# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse_lazy
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def base(request):
      return render(request,'reservation/base.html')
# # Vues pour Table
# class TableListView(ListView):
#     model = Table
#     template_name = 'reservation/table_list.html'

# class TableDetailView(DetailView):
#     model = Table
#     template_name = 'reservation/table_detail.html'

# class TableCreateView(CreateView):
#     model = Table
#     form_class = TableForm
#     template_name = 'reservation/table_form.html'
#     success_url = reverse_lazy('table_list')

# class TableUpdateView(UpdateView):
#     model = Table
#     form_class = TableForm
#     template_name = 'reservation/table_form.html'
#     success_url = reverse_lazy('table_list')

# class TableDeleteView(DeleteView):
#     model = Table
#     template_name = 'reservation/table_confirm_delete.html'
#     success_url = reverse_lazy('table_list')

# # Vues pour Reservation
# class ReservationListView(ListView):
#     model = Reservation
#     template_name = 'reservation/reservation_list.html'

# class ReservationDetailView(DetailView):
#     model = Reservation
#     template_name = 'reservation/reservation_detail.html'

# class ReservationCreateView(CreateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = 'reservation/reservation_form.html'
#     success_url = reverse_lazy('reservation_list')

# class ReservationUpdateView(UpdateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = 'reservation/reservation_form.html'
#     success_url = reverse_lazy('reservation_list')

# class ReservationDeleteView(DeleteView):
#     model = Reservation
#     template_name = 'reservation/reservation_confirm_delete.html'
#     success_url = reverse_lazy('reservation_list')

# # Exemple de fonction pour confirmer une réservation
# def confirmer_reservation(request, pk):
#     reservation = get_object_or_404(Reservation, pk=pk)
#     reservation.status = 'Confirmée'
#     reservation.save()
#     return redirect('reservation_detail', pk=reservation.pk)
# # Create your views here.
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.contrib import messages


# reservation/views.py

from django.shortcuts import redirect
from .models import Reservation
from .forms import ReservationForm
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .forms import ReservationForm
from users.models import Utilisateur, Client

from django.shortcuts import render, redirect
from django.urls import reverse
from reservation.forms import ReservationForm
from reservation.models import Reservation
from users.models import Utilisateur, Client
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ReservationForm  # Assure-toi que ce formulaire existe
from .models import Reservation

def reserver_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            # Envoi de l'e-mail de confirmation
            subject = "Confirmation de votre réservation"
            message = (
                f"Bonjour {reservation.nom},\n\n"
                f"Votre réservation du {reservation.date.strftime('%d/%m/%Y')} à {reservation.heure.strftime('%H:%M')} "
                f"pour {reservation.nombre_personnes} personne(s) a bien été reçue.\n"
                f"Type de table demandé : {reservation.type_table}.\n"
                f"Nous vous contacterons rapidement pour la confirmation.\n\n"
                "Merci pour votre confiance.\n"
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [reservation.email])
                messages.success(request, "Réservation enregistrée et email de confirmation envoyé.")
            except Exception as e:
                messages.warning(request, f"Réservation enregistrée, mais erreur lors de l'envoi de l'email : {e}")

            return redirect('home')  
    else:
        form = ReservationForm()

    return render(request, 'reservation/reserver_table.html', {'form': form})

from django.shortcuts import render
from .models import Reservation

def liste_reservations(request):
    reservations = Reservation.objects.all().order_by('-date')  
    return render(request, 'reservation/liste_reservations.html', {'reservations': reservations})
from django.shortcuts import render, get_object_or_404
from .models import Reservation

def detail_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation/detail_reservation.html', {'reservation': reservation})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation
from .forms import ReservationForm  

def modifier_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation:liste_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation/modifier_reservation.html', {'form': form})

def supprimer_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation:liste_reservations')
    return render(request, 'reservation/confirmer_suppression.html', {'reservation': reservation})
def confirmation(request):
    return render(request, 'reservation/confirmation.html')
