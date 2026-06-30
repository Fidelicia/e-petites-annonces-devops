from django.db import models
from django.contrib.auth.models import User
from math import radians, sin, cos, sqrt, atan2


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                                on_delete=models.CASCADE, related_name='sous_categories')
    icone = models.CharField(max_length=50, blank=True, default='tag')

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Annonce(models.Model):
    ETAT_CHOICES = [
        ('neuf', 'Neuf'),
        ('bon', 'Bon état'),
        ('moyen', 'État moyen'),
    ]
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('vendue', 'Vendue/Pourvue'),
        ('suspendue', 'Suspendue'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='annonces')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    ville = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default='bon')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='active')
    nb_vues = models.PositiveIntegerField(default=0)
    est_premium = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-est_premium', '-date_creation']

    def __str__(self):
        return self.titre

    def distance_km(self, lat, lon):
        if self.latitude is None or self.longitude is None:
            return None
        R = 6371
        dlat = radians(lat - self.latitude)
        dlon = radians(lon - self.longitude)
        a = sin(dlat / 2) ** 2 + cos(radians(lat)) * cos(radians(self.latitude)) * sin(dlon / 2) ** 2
        return R * 2 * atan2(sqrt(a), sqrt(1 - a))


class PhotoAnnonce(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='annonces/%Y/%m/')
    principale = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo de {self.annonce.titre}"


class Favori(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favorise_par')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'annonce')


class Message(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_envoi']


class Signalement(models.Model):
    MOTIF_CHOICES = [
        ('spam', 'Spam ou publicité'),
        ('frauduleux', 'Annonce frauduleuse'),
        ('inapproprie', 'Contenu inapproprié'),
        ('autre', 'Autre'),
    ]
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='signalements')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    motif = models.CharField(max_length=20, choices=MOTIF_CHOICES)
    commentaire = models.TextField(blank=True)
    date_signalement = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
