#!/bin/bash
set -e
echo "Application des migrations..."
python manage.py migrate --noinput
echo "Initialisation des categories..."
python manage.py init_categories || true
echo "Demarrage de Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:80 --workers 3
