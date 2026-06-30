# E-Petites-Annonces — Projet DevOps CI/CD

Plateforme de petites annonces (Madagascar) développée en Django, conteneurisée avec
Docker, intégrée et déployée automatiquement via Jenkins, exposée via Nginx.

## Structure du projet

```
projet-devops/
├── app/                  Code source Django (annonces, config, templates, static)
├── docker/
│   └── Dockerfile
├── nginx/
│   └── nginx.conf
├── Jenkinsfile           Pipeline CI/CD (Checkout, Build, Test, Deploy)
├── redeploy.sh           Script de redéploiement automatique
├── .gitignore
└── README.md
```

## Démarrage rapide en local (sans Docker)

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations annonces
python manage.py migrate
python manage.py init_categories
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Ouvrir http://localhost:8000

## Avec Docker

```bash
docker build -t app-devops -f docker/Dockerfile .
docker run -d --name app-devops-prod -p 8080:80 app-devops
```

Ouvrir http://localhost:8080

## Avec Nginx (reverse proxy)

```bash
docker network create reseau-devops
docker run -d --name app-devops-prod --network reseau-devops -p 8080:80 app-devops
docker run -d --name nginx-proxy --network reseau-devops -p 80:80 \
  -v $(pwd)/nginx/nginx.conf:/etc/nginx/conf.d/default.conf nginx:alpine
```

Ouvrir http://localhost

## Redéploiement automatique

```bash
./redeploy.sh
```

## Fonctionnalités

- Catégories d'annonces (Immobilier, Véhicules, Emplois, Services, Électronique, Mode)
- Publication d'annonces avec photos (Pillow), **validation des formats d'image**
  (jpg/jpeg/png/webp, fichiers corrompus ou non-images rejetés automatiquement)
- Recherche/filtres (django-filter) : mot-clé, catégorie, ville, prix, état
- Favoris, messagerie simple entre utilisateurs
- **Signalement d'annonces** (spam, frauduleuse, contenu/image inapproprié(e), autre)
- Carte globale des annonces géolocalisées (Folium) + **carte individuelle centrée sur le
  lieu exact de publication** sur chaque page de détail
- Compteur de vues par annonce
- Authentification complète (inscription / connexion / **déconnexion fonctionnelle** via
  formulaire POST sécurisé CSRF)
- **Interface responsive, charte graphique turquoise / jaune / blanc / noir**
- **Mode sombre et mode clair** (bouton de bascule, préférence mémorisée dans le navigateur)

