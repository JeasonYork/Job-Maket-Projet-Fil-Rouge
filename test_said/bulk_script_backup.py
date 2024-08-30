import os
import sys
import json
from elasticsearch import Elasticsearch, helpers

# Définir le chemin du fichier de log
log_file_path = '/home/ubuntu/elasticsearch/error.log'

# Rediriger la sortie standard et d'erreur vers le fichier de log
sys.stdout = open(log_file_path, 'a')
sys.stderr = open(log_file_path, 'a')

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
            print(f"Erreur d'importation du fichier {json_file_path}: {str(e)}")

# Fermer le fichier de log
sys.stdout.close()
sys.stderr.close()

print("Les données JSON ont été importées avec succès dans Elasticsearch.")
