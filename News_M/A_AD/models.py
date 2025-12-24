from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    # إضافة حقل اللون (Bootstrap classes)
    color = models.CharField(
        max_length=20,
        choices=[
            ("primary", "Bleu"),
            ("success", "Vert"),
            ("danger", "Rouge"),
            ("warning", "Jaune"),
            ("info", "Cyan"),
            ("secondary", "Gris"),
        ],
        default="secondary"
    )

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.titre

class Annonce(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='annonces/', blank=True, null=True)

    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class ContactMessage(models.Model):

    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"



class ActionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"



class CommandeAnnonce(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En attente'), ('validee', 'Validée'), ('refusee', 'Refusée')],
        default='en_attente'
    )

    def __str__(self):
        return f"Commande de {self.nom} - {self.annonce.titre}"