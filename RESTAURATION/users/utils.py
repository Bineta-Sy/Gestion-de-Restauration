from users.models import Utilisateur

def get_utilisateur_connecte(request):
    email = request.session.get('email')
    if email:
        try:
            return Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return None
    return None
