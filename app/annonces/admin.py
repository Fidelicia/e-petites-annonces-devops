from django.contrib import admin
from .models import Categorie, Annonce, PhotoAnnonce, Favori, Message, Signalement

admin.site.register(Categorie)
admin.site.register(Annonce)
admin.site.register(PhotoAnnonce)
admin.site.register(Favori)
admin.site.register(Message)
admin.site.register(Signalement)
