# Utiliser une image officielle Python slim comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu de l'application dans le répertoire de travail
COPY . .

# Définir la variable d'environnement ES_HOST
ENV ES_HOST=13.38.84.40:9200

# Ajouter /app au PYTHONPATH pour permettre les imports
ENV PYTHONPATH=/app

# Exposer le port sur lequel l'application va tourner
EXPOSE 5000

# Commande pour exécuter l'application Dash
CMD ["python3", "app/main.py"]
