import requests
import json

# Configuration
elasticsearch_host = 'http://localhost:9200'  # Adresse de votre instance Elasticsearch
index_name = 'jobmarket'                      # Nom de l'index
size = 1                                      # Nombre de documents à récupérer

def get_random_document(elasticsearch_host, index_name, size=1):
    url = f"{elasticsearch_host}/{index_name}/_search"
    query = {
        "size": size,
        "query": {
            "function_score": {
                "functions": [
                    {
                        "random_score": {}
                    }
                ]
            }
        }
    }

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(query))
        response.raise_for_status()  # Vérifie si la requête a échoué
        hits = response.json().get('hits', {}).get('hits', [])
        if hits:
            for hit in hits:
                print(json.dumps(hit['_source'], indent=2))
        else:
            print("Aucun document trouvé.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recherche de documents : {e}")

if __name__ == "__main__":
    get_random_document(elasticsearch_host, index_name, size)
