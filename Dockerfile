# Utilise une image Python de base
FROM python:3.9-slim
# Installer les dépendances système
RUN apt-get update && apt-get install -y libpq-dev gcc libexpat1

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires et installer les dépendances
#COPY src/ /app
COPY requirements.txt /app/requirements.txt
#COPY data /app/data
#COPY schema /app/schema
RUN pip install --no-cache-dir -r requirements.txt
# Copiez le script de démarrage dans le conteneur
COPY start.sh /start.sh

# Donne les permissions d'exécution au script
RUN chmod +x /start.sh
# Exposer le port par défaut de Flask
EXPOSE 5000

# Commande de démarrage de Flask
CMD ["/start.sh"]
#CMD ["flask", "run", "--host=0.0.0.0"]