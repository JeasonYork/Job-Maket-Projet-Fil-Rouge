#!/bin/bash

# Initialiser pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Chemin absolu vers le répertoire de votre projet
ENV_DIR="/home/ubuntu/test_mohamed"
PROJECT_DIR="/home/ubuntu/test_mohamed/wttj"

# Utiliser la version Python requise
pyenv shell 3.12.0

# Vérifier que Poetry utilise la bonne version de Python
poetry env use $(pyenv which python3.12)

# Régénérer le fichier poetry.lock si nécessaire
poetry lock

#Activer l'environnement virtuel de Poetry
poetry install

# Installer les navigateurs Playwright
poetry run playwright install
sudo playwright install-deps

# Aller dans le repertoire du projet
cd "$PROJECT_DIR"

# Lancer le script de scraping Python via Poetry avec la version spécifique de Python
echo "Script de scraping exécuté à $(date)" >> $PROJECT_DIR / scraping.log
poetry run python main_wttj.py



# Lancer le script de chargement dans Elasticsearch via Poetry avec la version spécifique de Python
echo "Script de chargement exécuté à $(date)" >> $PROJECT_DIR / elasticsearch.log
poetry run $PYTHON_PATH load_json.py

