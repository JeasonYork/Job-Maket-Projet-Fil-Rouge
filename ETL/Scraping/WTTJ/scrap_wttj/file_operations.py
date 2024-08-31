"""
Module containing all the functions related to the file operations (save but other if needed)
"""

from pathlib import Path
import json
import logging


# Configuration du journal dans un fichier
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration du journal pour afficher uniquement les erreurs dans la console
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def save_file(file_to_save, output_name: str):
    current_directory = Path(__file__).resolve().parent.parent
    output_name = f"{output_name}.json"
    output_directory = Path.joinpath(current_directory, "data")
    output_path = Path.joinpath(output_directory, output_name)

    try:
        # Vérifie si le répertoire de sortie existe, sinon le crée
        if not output_directory.exists():
            output_directory.mkdir(parents=True)

        # Si le fichier existe, lire son contenu et ajouter les nouvelles données à la liste existante
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_data.extend(file_to_save)
        else:
            existing_data = file_to_save

        # Écrire la liste mise à jour dans le fichier JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False)

        logging.warning(f"File saved to {output_path}")
    except Exception as e:
        logging.error(f"An error occured during saving : {e}")
