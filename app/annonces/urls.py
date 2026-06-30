from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonce/<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('annonce/<int:pk>/favori/', views.toggle_favori, name='toggle_favori'),
    path('annonce/<int:pk>/message/', views.envoyer_message, name='envoyer_message'),
    path('annonce/<int:pk>/signaler/', views.signaler_annonce, name='signaler_annonce'),
    path('carte/', views.carte_annonces, name='carte_annonces'),
    path('publier/', views.publier_annonce, name='publier_annonce'),
    path('mes-annonces/', views.mes_annonces, name='mes_annonces'),
    path('mes-favoris/', views.mes_favoris, name='mes_favoris'),
    path('messagerie/', views.messagerie, name='messagerie'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', auth_views.LoginView.as_view(template_name='annonces/connexion.html'), name='connexion'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
]
