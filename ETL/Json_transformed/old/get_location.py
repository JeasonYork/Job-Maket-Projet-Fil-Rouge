from pathlib import Path
import json

# Chemin du répertoire contenant le script courant
current_directory = Path(__file__).parent

# Fichier de sortie
output_file = current_directory / 'location.txt'

# Set pour stocker les valeurs uniques de la variable location
locations = set()

# Parcourir tous les fichiers JSON du répertoire
print(f"Recherche des fichiers JSON dans le répertoire : {current_directory}")

for fichier in current_directory.glob('*.json'):
    print(f"Lecture du fichier : {fichier}")
    try:
        # Ouvrir et lire le contenu du fichier JSON
        with fichier.open('r', encoding='utf-8') as f:
            data = json.load(f)
            # Vérifier si le fichier est une liste de dictionnaires
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'location' in item:
                        if item['location'] is not None:  # Filtrer les valeurs None
                            locations.add(str(item['location']))  # Ajouter au set
            else:
                print(f"Le contenu du fichier n'est pas une liste : {fichier}")
    except json.JSONDecodeError:
        print(f"Erreur de lecture du fichier JSON : {fichier}")

# Écrire les valeurs dans le fichier de sortie en les séparant par une virgule et un saut de ligne
with output_file.open('w', encoding='utf-8') as f:
    if locations:
        f.write(",\n".join(locations) + "\n")
    else:
        f.write("")

print(f"Les valeurs de 'location' ont été écrites dans{output_file}") 
