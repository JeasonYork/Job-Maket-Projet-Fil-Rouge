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


def remove_duplicates(file_path):
    unique_job_offers = []
    seen_job_offers = set()

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

    data_dir = Path(__file__).resolve().parent / "data"
    week_number = datetime.datetime.now().isocalendar()[1]
    file_path = data_dir / f"wttj_database_{week_number}.json"

    remove_duplicates(file_path)


if __name__ == "__main__":
    main()
