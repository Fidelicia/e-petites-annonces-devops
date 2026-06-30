import django_filters
from .models import Annonce, Categorie


class AnnonceFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='titre', lookup_expr='icontains', label='Mot-clé')
    categorie = django_filters.ModelChoiceFilter(queryset=Categorie.objects.all())
    ville = django_filters.CharFilter(field_name='ville', lookup_expr='icontains')
    prix_min = django_filters.NumberFilter(field_name='prix', lookup_expr='gte')
    prix_max = django_filters.NumberFilter(field_name='prix', lookup_expr='lte')
    etat = django_filters.ChoiceFilter(choices=Annonce.ETAT_CHOICES)

    class Meta:
        model = Annonce
        fields = ['q', 'categorie', 'ville', 'prix_min', 'prix_max', 'etat']
