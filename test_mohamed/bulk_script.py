import os
import sys
import json
from elasticsearch import Elasticsearch, helpers

# Définir le chemin du fichier de log
log_file_path = '/home/ubuntu/elasticsearch/error.log'

# Ouvrir le fichier de log pour redirection des sorties
sys.stdout = open(log_file_path, 'a')
sys.stderr = open(log_file_path, 'a')

def main():
    # Connexion à Elasticsearch
    es = Elasticsearch(
        hosts=["http://elastic:datascientest@localhost:9200"],
        verify_certs=False,
        ssl_show_warn=False
    )

    # Chemin vers le répertoire contenant les fichiers JSON
    json_directory_path = '/home/ubuntu/test_mohamed/bases'

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

# Appeler la fonction principale
if __name__ == "__main__":
    main()

    # Fermer les fichiers de log après que toutes les opérations soient terminées
    sys.stdout.close()
    sys.stderr.close()

    # Réinitialiser stdout et stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    print("Les données JSON ont été importées avec succès dans Elasticsearch.")
