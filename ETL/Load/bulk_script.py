import os
import json
import logging
from elasticsearch import Elasticsearch, helpers

# Configure logging to a file
logging.basicConfig(filename='/home/ubuntu/elasticsearch/error.log', level=logging.ERROR)

# Connexion à Elasticsearch
es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    verify_certs=False,
    ssl_show_warn=False
)

# Chemin vers le répertoire contenant les fichiers JSON
json_directory_path = '/home/ubuntu/test_said/Json'

# Fonction pour lire et charger le fichier JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Vérifier si l'index 'jobmarket' existe, sinon le créer
if not es.indices.exists(index='jobmarket'):
    try:
        # Créer l'index 'jobmarket'
        es.indices.create(index='jobmarket', ignore=400)
        print("Index 'jobmarket' créé avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'index 'jobmarket': {str(e)}")

# Chargement des données JSON
print("Importation des fichiers :")
for json_file in os.listdir(json_directory_path):
    if json_file.endswith(".json"):
        try:
            json_file_path = os.path.join(json_directory_path, json_file)
            json_data = load_json(json_file_path)
            helpers.bulk(es, json_data, index='jobmarket')
            print(f"{json_file} importé avec succès.")
        except Exception as e:
            logging.error(f"Erreur d'importation du fichier {json_file_path}: {str(e)}")

print("Les données JSON ont été importées avec succès dans Elasticsearch.")


