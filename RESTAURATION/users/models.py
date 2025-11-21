from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)
    ROLES = [
        ('ADMIN', 'Administrateur'),
        ('MANAGER', 'Manager'),
        ('SERVEUR', 'Serveur'),
        ('CUISINIER', 'Cuisinier'),
        ('LIVREUR', 'Livreur'),
        ('CLIENT', 'Client'),
    ]
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajout d'une valeur par défaut pour le rôle, qui sera écrasée par les sous-classes
    role = models.CharField(max_length=20, choices=ROLES)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


    def save(self, *args, **kwargs):
        # Ne re-hache que si ce n’est pas déjà un mot de passe crypté
        if not self.mot_de_passe.startswith('pbkdf2_'):
            self.mot_de_passe = make_password(self.mot_de_passe)
        super().save(*args, **kwargs)


    def __str__(self):
            return f"{self.prenom} {self.nom}   ({self.role} )"


class Client(Utilisateur):
    adresse = models.CharField(max_length=255, blank=True, null=True)
   
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'CLIENT'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Client: {self.prenom} {self.nom}"

class Administrateur(Utilisateur):
    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'ADMIN'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Administrateur: {self.prenom} {self.nom}"

class Manager(Utilisateur):
    # Relation : Un Manager est supervisé par un Administrateur
    admin_ref = models.ForeignKey(Administrateur, on_delete=models.CASCADE, related_name='managers')

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'MANAGER'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Manager: {self.prenom} {self.nom}"

class Cuisinier(Utilisateur):
    specialite = models.CharField(max_length=100)
    # Relation : Un Cuisinier est géré par un Manager
    manager_ref = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='cuisiniers')

    class Meta:
        verbose_name = "Cuisinier"
        verbose_name_plural = "Cuisiniers"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'CUISINIER'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Cuisinier: {self.prenom} {self.nom}"

class Serveur(Utilisateur):
    # Relation : Un Serveur est géré par un Manager
    manager_ref = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='serveurs')

    class Meta:
        verbose_name = "Serveur"
        verbose_name_plural = "Serveurs"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'SERVEUR'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Serveur: {self.prenom} {self.nom}"

class Livreur(Utilisateur):
    # Relation : Un Livreur est géré par un Manager
    manager_ref = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='livreurs')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Livreur"
        verbose_name_plural = "Livreurs"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = 'LIVREUR'
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Livreur: {self.prenom} {self.nom}"
    
##########System messagerie

class Message(models.Model):
    expediteur = models.ForeignKey(Utilisateur, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)  

    class Meta:
        ordering = ['-date_envoi']

    def __str__(self):
        return f"De {self.expediteur} à {self.destinataire} ({'lu' if self.lu else 'non lu'})"
