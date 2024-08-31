import asyncio
import datetime
import json
import logging
import logging.config
import sys
from pathlib import Path

from playwright.async_api import async_playwright
from scrap_wttj.constants import (
    COMPANY_INFO_SELECTOR,
    COMPANY_SELECTORS,
    CONTRACT_INFO_SELECTOR,
    CONTRACT_SELECTORS,
    JOB_LINK_SELECTOR,
    JOBS,
    RACINE_URL,
    RAW_DESCRIPTION_SELECTORS,
    TOTAL_PAGE_SELECTOR,
)
from scrap_wttj.data_extraction import (
    extract_links,
    get_company_elements,
    get_contract_elements,
    get_raw_description,
)
from scrap_wttj.file_operations import save_file
from scrap_wttj.pagination_functions import get_html, get_total_pages

current_dir = Path(__file__).resolve().parent

# Ensure output directories exist
log_dir = current_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
data_dir = current_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# Ensure log directory exists
log_file = log_dir / "scraper.log"

# Configuration du logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(log_file),
            "formatter": "default",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
    "loggers": {
        "my_lib": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Apply logging configuration
logging.config.dictConfig(logging_config)

checkpoint_file = data_dir / "checkpoint.json"


def save_checkpoint(job, page_number):
    with open(checkpoint_file, "w") as f:
        json.dump({"job": job, "page_number": page_number}, f)


def load_checkpoint():
    if checkpoint_file.exists():
        with open(checkpoint_file, "r") as f:
            return json.load(f)
    return None


async def generate_job_search_url(job, page_number):
    url = f"https://www.welcometothejungle.com/fr/jobs?query={job.replace(' ', '%20')}&page={page_number}&aroundQuery=worldwide"
    logging.info(f"Generated URL: {url}")
    return url


async def scrape_job_offers(page, job, page_number, final_file):
    job_search_url = await generate_job_search_url(job, page_number)
    logging.info(f"Scraping URL: {job_search_url}")
    try:
        await page.goto(job_search_url, timeout=30000)
        await page.wait_for_load_state("networkidle")
        job_links = await extract_links(page, job_search_url, JOB_LINK_SELECTOR)
        logging.info(f"Extracted job links: {job_links}")

        if not job_links:
            logging.warning(f"No job links found for URL: {job_search_url}")
            return []

        job_offers = []

        for link in job_links:
            if link is None:
                logging.error("Extracted link is None, skipping...")
                continue

            complete_url = f"{RACINE_URL}{link}"
            logging.info(f"Fetching job details from: {complete_url}")
            try:
                html = await get_html(complete_url)
                if html:
                    logging.info(f"Fetched HTML for {complete_url}")
                    job_offer = {
                        "source": "welcometothejungle",
                        **await get_contract_elements(
                            html, CONTRACT_INFO_SELECTOR, CONTRACT_SELECTORS
                        ),
                        "company_data": await get_company_elements(
                            html, COMPANY_INFO_SELECTOR, COMPANY_SELECTORS
                        ),
                        "description": await get_raw_description(
                            html, RAW_DESCRIPTION_SELECTORS
                        ),
                    }
                    job_offers.append(job_offer)

                    # Append each job offer to the JSON list in the final file
                    append_to_json_list(final_file, job_offer)
                    logging.info(f"Successfully wrote job offer to {final_file}")
                else:
                    logging.error(f"Failed to fetch HTML from {complete_url}, got None")

                await asyncio.sleep(0.5)

            except Exception as e:
                logging.error(f"Failed to fetch job details from {complete_url}: {e}")

        return job_offers

    except Exception as e:
        logging.error(f"Failed to scrape {job_search_url}: {e}")
        return []


def append_to_json_list(file_path, item):
    try:
        if (
            file_path.exists() and file_path.stat().st_size > 2
        ):  # If the file is not empty and not just '[]'
            with open(file_path, "r+", encoding="utf-8") as f:
                f.seek(0, 2)  # Go to the end of the file
                f.seek(
                    f.tell() - 1, 0
                )  # Move back one character (to before the last ])
                f.truncate()  # Remove the last character
                f.write(
                    ",\n"
                )  # Add a comma (to separate this from the previous dict) and a newline
                json.dump(item, f)  # Dump the new dictionary
                f.write("]")  # Close the list
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([item], f)  # Create a new list with the first item
    except Exception as e:
        logging.error(f"Error while appending to JSON list: {e}")


async def launch_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch()
    return browser, playwright


async def close_browser(browser, playwright):
    await browser.close()
    await playwright.stop()


async def scrape_jobs(page, final_file):
    checkpoint = load_checkpoint()
    if checkpoint:
        start_job = checkpoint["job"]
        start_page = checkpoint["page_number"]
        start_index = JOBS.index(start_job)
    else:
        start_index = 0
        start_page = 1

    for job in JOBS[start_index:]:
        baseurl = await generate_job_search_url(job, 1)
        total_pages = await get_total_pages(baseurl, TOTAL_PAGE_SELECTOR)
        if total_pages is None:
            logging.error(f"Could not determine total pages for job: {job}")
            continue
        for page_number in range(start_page, total_pages + 1):
            await scrape_job_offers(page, job, page_number, final_file)
            save_checkpoint(job, page_number)
        start_page = 1  # Reset page number after the first job


async def main():
    logger = logging.getLogger(__name__)

    # Determine the week number and final file name
    week_number = datetime.datetime.now().isocalendar()[1]
    final_file = data_dir / f"wttj_database_{week_number}.json"

    # Initialize final file with an empty list if it doesn't exist
    if not final_file.exists():
        with open(final_file, "w", encoding="utf-8") as f:
            f.write("[]")  # Initialize with empty list

    # Launch browser
    browser, playwright = await launch_browser()
    page = await browser.new_page()

    try:
        # Scrape jobs
        await scrape_jobs(page, final_file)
    finally:
        # Ensure browser is closed
        await close_browser(browser, playwright)


if __name__ == "__main__":
    asyncio.run(main())
    sys.exit()
