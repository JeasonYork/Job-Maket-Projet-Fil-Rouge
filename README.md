# webscraping_Jobmarket
Webscrapping des site Welcome to the Jungle, France Travail (ex pôle emploi), indeed et linkedIn dans le cadre du projet JobMarket pour la formation Data Engineer de DataScientest.

# Projet ETL pour l'analyse du marché de l'emploi dans les métiers de la data

## Introduction
Ce projet vise à développer une platforme pour analyser les offres d'emploi dans le secteur des métiers de la data. Le processus d'ETL permet d'extraire les nouvelles offres d'emploi quotidiennement, de les transformer et de les charger dans une base de données Elasticsearch. Cette base est accessible via deux APIs. Le projet s'appuie sur plusieurs technologies, notamment Docker, Elasticsearch, Dash, FastAPI et Airflow.

## Partie Extraction

### 1. Extraction Automatique des Données

L'extraction des données est gérée par deux cron jobs qui s'exécutent quotidiennement. Ces cron jobs permettent d'extraire automatiquement les nouvelles offres d'emploi à partir des sites suivants :

- **Welcome to the Jungle** : L'extraction est réalisée via un container Docker.
- **France Travail** : L'extraction est réalisée via un script Python.

### 2. Transformation et chargement des données dans Elasticsearch

Après l'extraction, les fichiers Json généré sont transformé par le script Transformation 
Data_cleaning.py, par la suite les fichiers transformés sont chargé dans la base par le script Bulk_script.py. Les deux script de transformation et de chargement sont automatisé par Airflow.

#### a. Lancement du container Elasticsearch

Le container Elasticsearch est utilisé pour le stockage des données extraites. Les étapes suivantes doivent être exécutées :

```bash
cd /home/ubuntu/elasticsearch
docker compose up -d
```

#### b. Lancement des Containers Dash et FastAPI

Les containers Dash et FastAPI sont utilisés pour gérer la présentation des données et l'API associée. Pour les lancer, suivez les étapes suivantes :

1. **Accédez au répertoire API :**

   Pour commencer, naviguez vers le répertoire où sont situés les scripts nécessaires pour créer et lancer les images Docker de chacune des APIs :

   ```bash
   cd /home/ubuntu/APIs/
   ```
   Avant de passer à l'étape suivante il faudra configurer l'adresse IP du server host pour chaque ficher Dockerfile pour chacune des APIs (MyDashAPI_app , MyFastAPI_app).
   
   ```bash
   # Définir la variable d'environnement ES_HOST
   ENV ES_HOST=xx.xx.xx.xx:9200
   ```

3. **Création des Images Docker :**

   Après avoir accédé au répertoire approprié (APIs), créez les images Docker nécessaires en exécutant le script `CreateImages.sh`. Ce script construira les images Docker qui contiennent toutes les dépendances 
   et configurations nécessaires pour Dash et FastAPI.

   Pour créer les images, utilisez la commande suivante :

   ```bash
   ./CreateImages.sh
   ```

   3. **Lancement des Containers :**

   Une fois les images Docker créées, vous devez lancer les containers correspondants. Ces containers hébergeront l'API de visualisation des données my-dash-app et l'API d'interfaçage my-fastapi-app qui permet 
   d'interagir avec les données.

   Pour lancer les containers, exécutez le script `Launch.sh` en utilisant la commande suivante :

   ```bash
   ./Launch.sh
   ```

#### c. Lancement du Container Airflow

Airflow est utilisé pour orchestrer les différentes tâches du pipeline ETL, notamment les étapes de transformation et de chargement des données extraites. Une fois que les cron jobs ont extrait les données, Airflow prend le relais pour exécuter quotidiennement ces tâches de manière automatisée.

Pour lancer le container Airflow, suivez les étapes suivantes :

1. **Accédez au répertoire Airflow :**

   Tout d'abord, naviguez vers le répertoire où se trouvent les fichiers de configuration d'Airflow :

   ```bash
   cd /home/ubuntu/airflow
   ```

2.**Démarrage du container Airflow :**
    
  Une fois dans le répertoire, executez le script init_airflow.sh

  ```bash
   ./init_airflow.sh
   ```
  
   puis démarrez le container Airflow en exécutant les commandes suivantes :

  ```bash
  docker network connect elasticsearch_es-net airflow_airflow-worker_1
  docker-compose up airflow-init
  docker-compose up -d
  ```

  Cette commande démarre Airflow en mode détaché, ce qui permet à Airflow de s’exécuter en arrière-plan.
    
  Le container Airflow orchestrera ensuite les tâches de transformation et de chargement des données, garantissant que les données extraites sont traitées et intégrées à Elasticsearch chaque jour.

  Avec Airflow en place, le pipeline ETL est entièrement automatisé, assurant une gestion fluide et continue du processus de traitement des données.

