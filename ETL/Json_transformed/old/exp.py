from pathlib import Path
import json

# Chemin du répertoire contenant le script courant
current_directory = Path(__file__).parent

# Fichier de sortie
output_file = current_directory / 'exp.txt'

# Set pour stocker les valeurs uniques de la variable experience
experiences = set()

# Parcourir tous les fichiers JSON du répertoire
print(f"Recherche des fichiers JSON dans le répertoire : {current_directory}")

for fichier in current_directory.glob('*_updated.json'):
    print(f"Lecture du fichier : {fichier}")
    try:
        # Ouvrir et lire le contenu du fichier JSON
        with fichier.open('r', encoding='utf-8') as f:
            data = json.load(f)
            # Vérifier si le fichier est une liste de dictionnaires
            if isinstance(data, list):
               for item in data:
                    if isinstance(item, dict) and 'experience' in item:
                        experience = item['experience']
                        if experience is not None:  # Filtrer les valeurs None
                            if isinstance(experience, list):  # Vérifier si l'expérience est une liste
                                for exp in experience:
                                    experiences.add(str(exp))  # Ajouter chaque élément au set
                            else:
                                experiences.add(str(experience))  # Ajouter au set
            else:
                print(f"Le contenu du fichier n'est pas une liste : {fichier}")
    except json.JSONDecodeError:
        print(f"Erreur de lecture du fichier JSON : {fichier}")

# Écrire les valeurs dans le fichier de sortie en les séparant par une virgule et un saut de ligne
with output_file.open('w', encoding='utf-8') as f:
    if experiences:
        f.write(",\n".join(experiences) + "\n")
    else:
        f.write("")

print(f"Les valeurs de 'experience' ont été écrites dans {output_file}")
