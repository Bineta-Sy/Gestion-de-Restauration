from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import qrcode
import base64
from django.urls import reverse

from .models import Facture
from commande.models import Commande
from users.models import Client


def base(request):
    return render(request, 'facturation/base.html')


def telecharger_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    template = get_template('facturation/facture_pdf.html')
    html = template.render({
        'facture': facture,
        'commande': facture.commande,
        'client': facture.commande.client,
        'plats': facture.commande.lignecommande_set.all()
    })

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'
        return response
    return HttpResponse("Erreur lors de la génération du PDF", status=500)

import base64
from io import BytesIO
import qrcode
from django.shortcuts import render, get_object_or_404, redirect
from commande.models import Commande
from facturation.models import Facture

def paiement_qr(request, commande_id=None):
    if commande_id is None:
        commande_id = request.session.get('commande_id')

    if not commande_id:
        return redirect('commande:voir_panier')  

    commande = get_object_or_404(Commande, id=commande_id)
    client = commande.client

    qr_data = f"Payez {commande.total} FCFA à Orange Money - N°: 77 000 00 00"
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer)
    img_qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    facture, created = Facture.objects.get_or_create(
        commande=commande,
        defaults={'montant_total': commande.total}
    )
    request.session['facture_id'] = facture.id
    request.session['commande_id'] = commande.id  

    return render(request, 'facturation/paiement_qr.html', {
        'qr_data': img_qr_base64,
        'montant_total': commande.total,
        'client': client,
        'facture': facture,
    })



def confirmer_paiement(request):
    if request.method == 'POST':
        facture_id = request.session.get('facture_id')
        if not facture_id:
            # Pas d'id facture en session, on renvoie à paiement QR
            return redirect('facturation:paiement_qr')

        # Récupérer la facture et mettre à jour son état paiement
        facture = get_object_or_404(Facture, id=facture_id)
        facture.est_payee = True  
        facture.save()
        return redirect('facturation:telecharger_facture', facture_id=facture.id)
    return redirect('facturation:paiement_qr')
