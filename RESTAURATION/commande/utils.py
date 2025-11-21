# commande/utils.py
from users.models import Client
from .models import Commande

def get_client_by_email(email):
    try:
        return Client.objects.get(email=email)
    except Client.DoesNotExist:
        return None

def get_panier_client_via_email(request):
    email = request.session.get('client_email')
    if not email:
        return None

    client = get_client_by_email(email)
    if not client:
        return None

    commande, created = Commande.objects.get_or_create(client=client, est_validee=False)
    return commande
