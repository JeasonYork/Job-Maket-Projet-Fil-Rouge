#!/bin/bash

# Creer les répertoires si ils n'existent pas
mkdir -p ./dags ./logs ./plugins

# Appliquer les permissions
chmod -R 777 ./logs
chmod -R 777 ./dags
chmod -R 777 ./plugins

# Creer le fichier .env avec les variables d'environnement
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

echo "Répertoires créés, permissions appliquées, et fichier .env généré."