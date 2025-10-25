#!/bin/bash
# Exécuter les migrations de base de données
sleep 50
flask db upgrade

flask load-schema run ./schema

# Démarrer Flask en arrière-plan
#flask run --host=0.0.0.0
gunicorn --workers=9 --bind=0.0.0.0:5000 app:app