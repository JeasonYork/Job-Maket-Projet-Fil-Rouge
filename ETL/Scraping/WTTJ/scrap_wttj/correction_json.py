import json

# Spécifiez le chemin du fichier JSON d'entrée et de sortie
chemin_du_fichier_entrée = '/Users/MoG/PycharmProjects/jobmarket/jobmarket/scrap_wttj/wttj_database_bronze_with_duplicates.json'
chemin_du_fichier_sortie = '/Users/MoG/PycharmProjects/jobmarket/jobmarket/scrap_wttj/wttj_database_bronze_with_duplicates_corrige.json'

# Chargez le fichier JSON d'entrée
with open(chemin_du_fichier_entrée, 'r') as fichier_entrée:
    donnees_json = fichier_entrée.readlines()

# Ajoutez les virgules manquantes
donnees_json_corrigees = [ligne.strip() + ',' for ligne in donnees_json]

# Écrivez le fichier JSON corrigé
with open(chemin_du_fichier_sortie, 'w') as fichier_sortie:
    fichier_sortie.write('\n'.join(donnees_json_corrigees))
