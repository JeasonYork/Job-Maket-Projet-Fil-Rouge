import json
import datetime
from pathlib import Path
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_duplicates(data):
    """Supprime les doublons dans une liste de dictionnaires."""
    seen = set()
    unique_data = []
    for d in data:
        json_str = json.dumps(d, sort_keys=True)  # Convertit le dict en chaîne JSON
        if json_str not in seen:
            seen.add(json_str)
            unique_data.append(d)
    return unique_data

def process_chunk(chunk, chunk_index):
    """Traitement parallèle pour un chunk de données."""
    unique_chunk = remove_duplicates(chunk)
    logging.info(f"Chunk {chunk_index} traité avec {len(unique_chunk)} éléments uniques.")
    return unique_chunk

def parallel_remove_duplicates(data, chunk_size=100):
    """Supprime les doublons en parallèle par chunks."""
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    unique_data = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_chunk, chunk, index): index for index, chunk in enumerate(chunks)}
        for future in as_completed(futures):
            unique_data.extend(future.result())

    return remove_duplicates(unique_data)  # Supprime les doublons finaux après combinaison des résultats

def load_json(file_path):
    """Charge un fichier JSON et retourne son contenu."""
    logging.info(f"Chargement du fichier JSON : {file_path}")
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """Sauvegarde les données dans un fichier JSON."""
    logging.info(f"Sauvegarde des données dans le fichier : {file_path}")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def compare_and_update_files(file_yesterday, file_today, chunk_size=100):
    # Charger les fichiers JSON
    data_yesterday = load_json(file_yesterday)
    data_today = load_json(file_today)

    # Supprimer les doublons dans chaque fichier en parallèle
    logging.info("Suppression des doublons en parallèle.")
    data_yesterday = parallel_remove_duplicates(data_yesterday, chunk_size)
    data_today = parallel_remove_duplicates(data_today, chunk_size)

    # Comparer les deux fichiers pour ne garder que les éléments qui sont dans le fichier du jour et pas celui de la veille
    logging.info("Comparaison des fichiers pour trouver les éléments uniques au fichier du jour.")
    unique_today = [item for item in data_today if json.dumps(item, sort_keys=True) not in {json.dumps(d, sort_keys=True) for d in data_yesterday}]

    # Mettre à jour le fichier du jour avec uniquement les nouvelles offres
    save_json(unique_today, file_today)
    logging.info(f"Le fichier {file_today} a été mis à jour avec les éléments uniques du jour.")

def main():
    # Chemin vers le dossier de sortie
    output_dir = Path("/app/Json_scraping")

    # Obtenir la date actuelle et la date d'hier sous forme de chaîne formatée
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    current_file_path = output_dir / f"wttj_database_{current_date}.json"
    yesterday_file_path = output_dir / f"wttj_database_{yesterday_date}.json"

    # Comparer les fichiers et mettre à jour le fichier du jour
    compare_and_update_files(yesterday_file_path, current_file_path)

if __name__ == "__main__":
    main()
