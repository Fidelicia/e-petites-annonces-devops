#!/bin/bash
set -e

echo "=== Arrêt de l'ancien conteneur ==="
docker stop app-devops-prod || true
docker rm app-devops-prod || true

echo "=== Reconstruction de l'image ==="
docker build -t app-devops -f docker/Dockerfile .

echo "=== Création du réseau (si besoin) ==="
docker network create reseau-devops || true

echo "=== Redéploiement ==="
docker run -d --name app-devops-prod --network reseau-devops -p 8080:80 app-devops

echo "=== Déploiement terminé. Application disponible sur http://localhost:8080 (ou http://localhost via Nginx) ==="
