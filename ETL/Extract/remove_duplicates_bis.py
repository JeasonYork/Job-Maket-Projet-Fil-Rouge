import datetime
import json
import logging
from pathlib import Path


def make_hashable(data):
    if isinstance(data, dict):
        return tuple((key, make_hashable(value)) for key, value in sorted(data.items()))
    elif isinstance(data, list):
        return tuple(make_hashable(item) for item in data)
    else:
        return data


def remove_duplicates(file_path, yesterday_job_offers):
    unique_job_offers = []
    seen_job_offers = set(make_hashable(offer) for offer in yesterday_job_offers)

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            job_offers = json.load(f)
            for job_offer in job_offers:
                hashable_job_offer = make_hashable(job_offer)
                if hashable_job_offer not in seen_job_offers:
                    unique_job_offers.append(job_offer)
                    seen_job_offers.add(hashable_job_offer)

    # Overwrite the final file with unique job offers
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(unique_job_offers, f, indent=4)
    logging.info(
        f"Successfully removed duplicates and wrote unique job offers to {file_path}"
    )


def main():
    logging.basicConfig(level=logging.INFO)
    # Chemin vers le dossier de sortie
    output_dir = Path("/home/ubuntu/ETL/Json_scraping")

    # Obtenir la date actuelle et la date d'hier sous forme de chaîne formatée
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    current_file_path = output_dir / f"wttj_database_{current_date}.json"
    yesterday_file_path = output_dir / f"wttj_database_{yesterday_date}.json"

    # Charger les offres d'emploi d'hier
    if yesterday_file_path.exists():
        with open(yesterday_file_path, "r", encoding="utf-8") as f:
            yesterday_job_offers = json.load(f)
    else:
        yesterday_job_offers = []

    # Supprimer les doublons en tenant compte des offres d'hier
    remove_duplicates(current_file_path, yesterday_job_offers)


if __name__ == "__main__":
    main()
