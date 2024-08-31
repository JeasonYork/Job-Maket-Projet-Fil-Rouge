import requests

# Configuration
elasticsearch_host = 'http://localhost:9200'  # Adresse de votre instance Elasticsearch
index_name = 'jobmarket'                      # Nom de l'index à supprimer

def delete_index(elasticsearch_host, index_name):
    url = f"{elasticsearch_host}/{index_name}"
    response = requests.delete(url)
    
    if response.status_code == 200:
        print(f"Index '{index_name}' supprimé avec succès.")
    elif response.status_code == 404:
        print(f"Index '{index_name}' non trouvé.")
    else:
        print(f"Erreur lors de la suppression de l'index '{index_name}'. Code de statut : {response.status_code}")
        print("Détails de l'erreur : ", response.json())

if __name__ == "__main__":
    delete_index(elasticsearch_host, index_name)
