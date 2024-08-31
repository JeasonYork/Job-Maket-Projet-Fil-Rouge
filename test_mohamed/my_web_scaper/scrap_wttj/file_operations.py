"""
Module containing all the functions related to the file operations (save but other if needed)
"""

import json
import logging
from pathlib import Path

# Configuration du journal dans un fichier
logger = logging.getLogger("scrap_wttj.file_operations")


def save_file(file_to_save, output_path: Path):
    try:
        # Si le fichier existe, lire son contenu et ajouter les nouvelles données à la liste existante
        if output_path.exists():
            with open(output_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                existing_data.extend(file_to_save)
        else:
            existing_data = file_to_save

        # Écrire la liste mise à jour dans le fichier JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        logger.info(f"File saved to {output_path}")
    except Exception as e:
        logger.error(f"An error occurred during saving: {e}")
