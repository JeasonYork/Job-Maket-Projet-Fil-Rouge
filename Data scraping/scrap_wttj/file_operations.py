"""
Module containing all the functions related to the file operations (save but other if needed)
"""

from pathlib import Path
import json
import logging


def save_file(file_to_save, output_name: str):
    current_directory = Path(__file__).resolve().parent
    output_name = f"{output_name}.json"
    output_path = Path.joinpath(current_directory, output_name)

    try:
        # Ouvre le fichier en mode écriture
        with open(output_path, 'a', encoding='utf-8') as fichier:
            # On utilise json.dump pour écrire les données dans le fichier JSON
            json.dump(file_to_save, fichier, ensure_ascii=False)
            fichier.write('\n')

        logging.info(f"File saved to {output_path}")
    except Exception as e:
        logging.info(f"An error occured during saving : {e}")
