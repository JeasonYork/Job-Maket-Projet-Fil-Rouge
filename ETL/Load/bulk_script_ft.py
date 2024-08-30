import os
import json
import logging
import argparse
from elasticsearch import Elasticsearch, helpers

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def main(json_file_path, log_file_path):
    # Configure logging to a file
    logging.basicConfig(filename=log_file_path, level=logging.ERROR)

    # Connexion à Elasticsearch
    es = Elasticsearch(
        hosts=["http://es-container:9200"],
        verify_certs=False,
        ssl_show_warn=False
    )

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
    try:
        json_data = load_json(json_file_path)
        helpers.bulk(es, json_data, index='jobmarket')
        print(f"{json_file_path} importé avec succès.")
    except Exception as e:
        logging.error(f"Erreur d'importation du fichier {json_file_path}: {str(e)}")

    print("Les données JSON ont été importées avec succès dans Elasticsearch.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk load JSON files into Elasticsearch.")
    parser.add_argument("json_file", type=str, help="Path to the JSON file")
    parser.add_argument("log_file", type=str, help="Path to the log file")

    args = parser.parse_args()

    main(args.json_file, args.log_file)
