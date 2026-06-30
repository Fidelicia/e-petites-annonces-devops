from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import F
from PIL import Image, UnidentifiedImageError
import folium

from .models import Annonce, Categorie, PhotoAnnonce, Favori, Message, Signalement
from .filters import AnnonceFilter

EXTENSIONS_AUTORISEES = ('.jpg', '.jpeg', '.png', '.webp')


def image_valide(fichier):
    """Vérifie que le fichier envoyé est bien une image lisible et dans un format autorisé."""
    nom = fichier.name.lower()
    if not nom.endswith(EXTENSIONS_AUTORISEES):
        return False
    try:
        fichier.seek(0)
        Image.open(fichier).verify()
        fichier.seek(0)
        return True
    except (UnidentifiedImageError, OSError):
        return False


def accueil(request):
    annonces = Annonce.objects.filter(statut='active')[:12]
    categories = Categorie.objects.filter(parent__isnull=True)
    return render(request, 'annonces/accueil.html', {
        'annonces': annonces,
        'categories': categories,
    })


def liste_annonces(request):
    qs = Annonce.objects.filter(statut='active')
    annonce_filter = AnnonceFilter(request.GET, queryset=qs)
    categories = Categorie.objects.filter(parent__isnull=True)
    return render(request, 'annonces/liste.html', {
        'filter': annonce_filter,
        'categories': categories,
    })


def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    Annonce.objects.filter(pk=pk).update(nb_vues=F('nb_vues') + 1)
    annonce.refresh_from_db()
    est_favori = False
    if request.user.is_authenticated:
        est_favori = Favori.objects.filter(utilisateur=request.user, annonce=annonce).exists()

    carte_html = None
    if annonce.latitude is not None and annonce.longitude is not None:
        m = folium.Map(location=[annonce.latitude, annonce.longitude], zoom_start=13)
        folium.Marker(
            [annonce.latitude, annonce.longitude],
            popup=annonce.titre,
            tooltip="Lieu de publication de l'annonce",
            icon=folium.Icon(color='cadetblue', icon='tag'),
        ).add_to(m)
        carte_html = m._repr_html_()

    return render(request, 'annonces/detail.html', {
        'annonce': annonce,
        'est_favori': est_favori,
        'carte_html': carte_html,
    })


def carte_annonces(request):
    qs = Annonce.objects.filter(statut='active', latitude__isnull=False, longitude__isnull=False)
    m = folium.Map(location=[-18.8792, 47.5079], zoom_start=6)
    for a in qs:
        folium.Marker(
            [a.latitude, a.longitude],
            popup=f"<b>{a.titre}</b><br>{a.prix} Ar<br><a href='/annonce/{a.pk}/'>Voir</a>",
            tooltip=a.titre,
        ).add_to(m)
    carte_html = m._repr_html_()
    return render(request, 'annonces/carte.html', {'carte_html': carte_html})


@login_required
def publier_annonce(request):
    categories = Categorie.objects.all()
    if request.method == 'POST':
        annonce = Annonce.objects.create(
            titre=request.POST['titre'],
            description=request.POST['description'],
            prix=request.POST['prix'],
            categorie_id=request.POST['categorie'],
            auteur=request.user,
            ville=request.POST['ville'],
            latitude=request.POST.get('latitude') or None,
            longitude=request.POST.get('longitude') or None,
            etat=request.POST.get('etat', 'bon'),
        )
        photos_rejetees = []
        for i, fichier in enumerate(request.FILES.getlist('photos')):
            if image_valide(fichier):
                PhotoAnnonce.objects.create(annonce=annonce, image=fichier, principale=(i == 0))
            else:
                photos_rejetees.append(fichier.name)
        if photos_rejetees:
            messages.warning(
                request,
                f"Fichier(s) ignoré(s) car non compatibles (formats acceptés : jpg, jpeg, png, webp) : "
                f"{', '.join(photos_rejetees)}"
            )
        messages.success(request, "Annonce publiée avec succès.")
        return redirect('detail_annonce', pk=annonce.pk)
    return render(request, 'annonces/publier.html', {'categories': categories})


@login_required
def mes_annonces(request):
    annonces = Annonce.objects.filter(auteur=request.user)
    return render(request, 'annonces/mes_annonces.html', {'annonces': annonces})


@login_required
def toggle_favori(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    fav, created = Favori.objects.get_or_create(utilisateur=request.user, annonce=annonce)
    if not created:
        fav.delete()
        messages.info(request, "Retiré des favoris.")
    else:
        messages.success(request, "Ajouté aux favoris.")
    return redirect('detail_annonce', pk=pk)


@login_required
def mes_favoris(request):
    favoris = Favori.objects.filter(utilisateur=request.user).select_related('annonce')
    return render(request, 'annonces/favoris.html', {'favoris': favoris})


@login_required
def envoyer_message(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    if request.method == 'POST':
        Message.objects.create(
            annonce=annonce,
            expediteur=request.user,
            destinataire=annonce.auteur,
            contenu=request.POST['contenu'],
        )
        messages.success(request, "Message envoyé.")
    return redirect('detail_annonce', pk=pk)


@login_required
def messagerie(request):
    envoyes = Message.objects.filter(expediteur=request.user)
    recus = Message.objects.filter(destinataire=request.user)
    return render(request, 'annonces/messagerie.html', {'envoyes': envoyes, 'recus': recus})


@login_required
def signaler_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    if request.method == 'POST':
        Signalement.objects.create(
            annonce=annonce,
            auteur=request.user,
            motif=request.POST['motif'],
            commentaire=request.POST.get('commentaire', ''),
        )
        messages.success(request, "Signalement envoyé, merci.")
    return redirect('detail_annonce', pk=pk)


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'annonces/inscription.html', {'form': form})
