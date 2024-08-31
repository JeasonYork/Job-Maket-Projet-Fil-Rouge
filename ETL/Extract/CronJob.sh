# Execute le sraping des offres du site welcome to the jumgle tous les jours à 3 heures du matin
0 3 * * * /home/ubuntu/ETL/run_scraping.sh >> /home/ubuntu/ETL/run_scraping.log 2>&1
