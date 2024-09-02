# Execute le scraping des offres du site welcome to the jungle tous les jours à 3 heures du matin
0 3 * * * /home/ubuntu/ETL/run_scraping.sh >> /home/ubuntu/ETL/run_scraping.log 2>&1

# Execute le scraping des offres du site france travail tous les jours à 6 heures du matin pour un pipeline automatisé avec airflow

0 6 * * * /home/ubuntu/ETL/ETL/Extract/FranceTravail/main_airflow.py

# Execute le scraping des offres du site france travail tous les jours à 6 heures du matin (pipeline python)

#0 6 * * * /home/ubuntu/ETL/ETL/Extract/FranceTravail/main.py
