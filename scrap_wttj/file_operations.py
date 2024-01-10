"""
Module containing all the functions related to the file operations (save but other if needed)
"""

from pathlib import Path
import json


def save_file(file_to_save, output_name: str):
    current_directory = Path(__file__).resolve().parent
    output_name = f"{output_name}.json"
    output_path = Path.joinpath(current_directory, output_name)

    try:
        # Ouvre le fichier en mode écriture
        with open(output_path, 'w', encoding='utf-8') as fichier:
            # On utilise json.dump pour écrire les données dans le fichier JSON
            json.dump(file_to_save, fichier, ensure_ascii=False)

        print(f"Le document a été enregistré avec succès dans {output_path}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du document : {e}")
