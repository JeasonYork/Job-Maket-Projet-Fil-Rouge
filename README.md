# webscraping_Jobmarket
Webscrapping des site Welcome to the Jungle, France Travail (ex pôle emploi), indeed et linkedIn dans le cadre du projet JobMarket pour la formation Data Engineer de DataScientest.

# Projet ETL pour l'analyse du marché de l'emploi dans les métiers de la data

## Introduction
Ce projet vise à développer un pipeline ETL (Extraction, Transformation, Chargement) pour analyser les offres d'emploi dans le secteur des métiers de la data. Le processus d'ETL permet d'extraire les nouvelles offres d'emploi quotidiennement, de les transformer et de les charger dans une base de données accessible via une API. Le projet s'appuie sur plusieurs technologies, notamment Docker, Elasticsearch, Dash, FastAPI et Airflow.

## Partie Extraction

### 1. Extraction Automatique des Données

L'extraction des données est gérée par deux cron jobs qui s'exécutent quotidiennement. Ces cron jobs permettent d'extraire automatiquement les nouvelles offres d'emploi à partir des sites suivants :

- **Welcome to the Jungle** : L'extraction est réalisée via un container Docker.
- **France Travail** : L'extraction est réalisée via un script Python.

### 2. Lancement des Containers Docker

Après l'extraction, il est nécessaire de lancer plusieurs containers Docker pour assurer le stockage, la présentation des données et la gestion de l'API.

#### a. Lancement du container Elasticsearch

Le container Elasticsearch est utilisé pour le stockage des données extraites. Les étapes suivantes doivent être exécutées :

```bash
cd /home/ubuntu/elasticsearch
docker compose up -d
```

#### b. Lancement des Containers Dash et FastAPI

Les containers Dash et FastAPI sont utilisés pour gérer la présentation des données et l'API associée. Pour les lancer, suivez les étapes suivantes :

1. **Accédez au répertoire API :**

   Pour commencer, naviguez vers le répertoire où sont situés les scripts nécessaires pour créer et lancer les images Docker :

   ```bash
   cd /home/ubuntu/API/
   ```

2. **Création des Images Docker :**

   Après avoir accédé au répertoire approprié, créez les images Docker nécessaires en exécutant le script `CreateImages.sh`. Ce script construira les images Docker qui contiennent toutes les dépendances et configurations nécessaires pour Dash et FastAPI.

   Pour créer les images, utilisez la commande suivante :

   ```bash
   ./CreateImages.sh
   ```

   3. **Lancement des Containers :**

   Une fois les images Docker créées, vous devez lancer les containers correspondants. Ces containers hébergeront l'application Dash, qui est utilisée pour la présentation des données, ainsi que l'API FastAPI, qui permet de gérer les requêtes et d'interagir avec les données.

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
    
  Une fois dans le répertoire, démarrez le container Airflow en exécutant la commande suivante :

  ```bash
  docker compose up -d
  ```

  Cette commande démarre Airflow en mode détaché, ce qui permet à Airflow de s’exécuter en arrière-plan.
    
  Le container Airflow orchestrera ensuite les tâches de transformation et de chargement des données, garantissant que les données extraites sont traitées et intégrées à l'API chaque jour.

Avec Airflow en place, le pipeline ETL est entièrement automatisé, assurant une gestion fluide et continue du processus de traitement des données.

