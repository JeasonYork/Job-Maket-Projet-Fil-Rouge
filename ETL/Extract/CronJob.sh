# Execute le sraping des offres du site welcome to the jumgle tous les jours à 3 heures du matin
0 3 * * * /home/ubuntu/ETL/Extract/run_docker_compose.sh >> /home/ubuntu/ETL/Extract/docker_compose_cron.log 2>&1
