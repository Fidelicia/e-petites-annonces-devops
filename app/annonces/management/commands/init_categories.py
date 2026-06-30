from django.core.management.base import BaseCommand
from annonces.models import Categorie


class Command(BaseCommand):
    help = "Crée les catégories de base"

    def handle(self, *args, **kwargs):
        categories = ['Immobilier', 'Véhicules', 'Emplois', 'Services', 'Électronique', 'Mode']
        for nom in categories:
            slug = nom.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e')
            Categorie.objects.get_or_create(nom=nom, slug=slug)
        self.stdout.write(self.style.SUCCESS('Catégories créées.'))
