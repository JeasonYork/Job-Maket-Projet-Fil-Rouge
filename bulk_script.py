from elasticsearch import Elasticsearch, helpers
import os
import json

# Connexion à Elasticsearch dans un conteneur Docker
# Verifier que le port 9200 est bien mappé sur la VM pour y accéder localement
# es = Elasticsearch(hosts=["http://localhost:9200"])

es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"],
    #use_ssl=True,                # Indique que SSL est utilisé
    verify_certs=False,          # Désactive la vérification des certificats
    ssl_show_warn=False          # Désactive les avertissements de sécurité SSL
)

# Chemin vers le fichier JSON
json_directory_path = 'JSON_AUTO'

# Fonction pour lire et charger le fichier JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

# Chargement des données JSON
print("importation des fichiers :")
for json_file in os.listdir(json_directory_path):
    if json_file.endswith(".json"):
        # Construire le chemin complet du fichier
        try:
            json_file_path = os.path.join(json_directory_path, json_file)

        # Charger les données JSON
            json_data = load_json(json_file_path)
            helpers.bulk(es, json_data, index='jobmarket')
            print(f"{json_file} importé avec succès.")
        except Exception as e :
            print(f"Erreur d'importation du fichier  {json_file_path}: {str(e)}")

# Verifier que l'index 'jobmarket' existe

print("Les données JSON ont été importées avec succès dans Elasticsearch.")