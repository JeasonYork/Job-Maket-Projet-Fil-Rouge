import os
import json
import logging
import argparse
from elasticsearch import Elasticsearch, helpers

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def remove_duplicates_in_index(es, index_name, source_field):
    """Supprime les doublons dans l'index Elasticsearch basé sur le champ source."""
    logging.info(f"Suppression des doublons dans l'index {index_name} pour source={source_field}.")
    
    # Requête pour trouver tous les documents où source = source_field
    query = {
        "query": {
            "match": {
                "source": source_field
            }
        }
    }
    
    # Recherche de tous les documents correspondants
    response = es.search(index=index_name, body=query, size=10000)  # Ajustez le `size` en fonction de vos besoins
    
    # Stocker les ID des documents déjà vus
    seen = set()
    for hit in response['hits']['hits']:
        _id = hit["_id"]
        source_data = json.dumps(hit["_source"], sort_keys=True)
        
        if source_data in seen:
            # Si le document est un doublon, on le supprime
            es.delete(index=index_name, id=_id)
            logging.info(f"Document ID {_id} supprimé.")
        else:
            seen.add(source_data)

def load_bulk_files(json_file_path, log_file_path):
    # Configure logging to a file
    logging.basicConfig(filename=log_file_path, level=logging.INFO)

    # Connexion à Elasticsearch
    es = Elasticsearch(
        hosts=["http://es-container:9200"],
        verify_certs=False,
        ssl_show_warn=False
    )

    # Chargement du fichier JSON dans Elasticsearch
    print(f"Importation du fichier : {json_file_path}")
    try:
        json_data = load_json(json_file_path)

        # Validation du format des données JSON
        if isinstance(json_data, list) and all(isinstance(doc, dict) for doc in json_data):
            helpers.bulk(es, json_data, index='jobmarket')
            print(f"{json_file_path} importé avec succès.")
        else:
            logging.error(f"Le fichier {json_file_path} ne contient pas une liste de documents JSON valides.")
            print(f"Erreur: Le fichier {json_file_path} ne contient pas une liste de documents JSON valides.")

    except json.JSONDecodeError as jde:
        logging.error(f"Erreur lors de la lecture du fichier JSON {json_file_path}: {str(jde)}")
        print(f"Erreur: Fichier JSON mal formaté {json_file_path}.")
    except Exception as e:
        logging.error(f"Erreur d'importation du fichier {json_file_path}: {str(e)}")
        print(f"Erreur: Échec de l'importation du fichier {json_file_path}.")

    print("Les données JSON ont été importées avec succès dans Elasticsearch.")

    # Supprimer les doublons après l'importation
    remove_duplicates_in_index(es, 'jobmarket', 'welcometothejungle')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk load JSON files into Elasticsearch.")
    parser.add_argument("json_file", type=str, help="Path to the JSON file")
    parser.add_argument("log_file", type=str, help="Path to the log file")
    args = parser.parse_args()

    load_bulk_files(args.json_file, args.log_file)
