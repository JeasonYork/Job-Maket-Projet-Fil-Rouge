#!/bin/bash

# Démarrer Elasticsearch et Kibana
cd ~/elasticsearch
docker-compose up -d

# Temporiser jusqu'à ce que Elasticsearch soit disponible
echo "En attente de la disponibilité d'Elasticsearch..."
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"yellow"\|"status":"green"'; do
  echo -n "."
  sleep 5
done

echo "Elasticsearch est disponible."

# Démarrer my-dash-app
cd ~/APIs/MyDashAPI_app
docker build -t my-dash-app .
docker run -d --name my-dash-app --network elasticsearch_es-net -p 5000:5000 my-dash-app

# Démarrer my-fastapi-app
cd ~/APIs/MyFastAPI_app
docker build -t my-fastapi-app .
docker run -d --name my-fastapi-app --network elasticsearch_es-net -p 8000:8000 my-fastapi-app

echo "Tous les services sont démarrés."
