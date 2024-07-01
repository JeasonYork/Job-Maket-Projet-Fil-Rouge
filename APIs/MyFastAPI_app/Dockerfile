# Utiliser une image officielle d'Ubuntu comme base
FROM ubuntu:22.04

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier le contenu de votre application dans le répertoire de travail
COPY . .

# Définir la variable d'environnement ES_HOST
ENV ES_HOST=13.60.31.28:9200

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

