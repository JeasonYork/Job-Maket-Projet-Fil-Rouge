import json
import datetime
from pathlib import Path
from elasticsearch import Elasticsearch

# Définir le chemin du fichier de log
log_path_file = 'home/ubuntu/elasticsearch/error.log'

# Rediriger la sortie standard et d'erreur vers le fichier de log
sys.stdout = open(log_file_path, 'a')
sys.stderr = open(log_file_path, 'a')

# Connexion à Elasticsearch
es = Elasticsearch(
    hosts=["http://elastic:datascientest@localhost:9200"], 
    verify_certs=False,
    ssl_show_warn=False
    )

def get_current_week():
    """Retourne le numéro de la semaine courante."""
    return datetime.datetime.now().isocalendar()[1]

def load_json_to_elasticsearch(directory, es_index):
    """Charge les fichiers JSON de la semaine courante dans Elasticsearch."""
    current_week = get_current_week()
    es = Elasticsearch()

    # Définir le chemin du répertoire contenant les fichiers JSON
    directory_path = Path(directory)
    
    for file_path in directory_path.glob('*.json'):
        # Suppose que le nom de fichier contient le numéro de semaine sous la forme `data_<week_number>.json`
        week_number = int(file_path.stem.split('_')[1])
        if week_number == current_week:
            with file_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    es.index(index=es_index, body=entry)
            print(f"Fichier {file_path.name} chargé avec succès.")
        else:
            print(f"Fichier {file_path.name} ignoré, car pas de la semaine courante.")

if __name__ == "__main__":
    # Utiliser Path(__file__).parent pour obtenir le répertoire du script actuel
    current_directory = Path(__file__).parent
    # Définir le chemin du répertoire data
    directory = current_directory.joinpath('data')
    es_index = f"jobmarket_week_{current_week}"
    load_json_to_elasticsearch(directory, es_index)
