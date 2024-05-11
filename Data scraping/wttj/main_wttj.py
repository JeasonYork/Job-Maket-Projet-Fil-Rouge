import sys
from pathlib import Path
import datetime

# Add the path of the parent directory to sys.path using pathlib
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

import logging
import sys
import asyncio
from scrap_wttj.constants import (JOBS, RACINE_URL, TOTAL_PAGE_SELECTOR, JOB_LINK_SELECTOR,
                                  CONTRACT_INFO_SELECTOR,
                                  COMPANY_INFO_SELECTOR, CONTRACT_SELECTORS, COMPANY_SELECTORS, SKILLS_DICT,
                                  JOB_DESCRIPTION_SELECTOR)
from playwright.async_api import async_playwright
from scrap_wttj.data_extraction import extract_links, get_contract_elements, get_company_elements, get_job_skills, \
    get_raw_description
from scrap_wttj.pagination_functions import get_total_pages, get_html
from scrap_wttj.file_operations import save_file


# Configuration du journal dans un fichier
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration du journal pour afficher uniquement les erreurs dans la console
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

async def generate_job_search_url(job, page_number):
    return f"https://www.welcometothejungle.com/fr/jobs?query={job.replace(' ', '%20')}&page={page_number}&aroundQuery=worldwide"


async def main():

    all_job_offers = []
    for job in JOBS:
        baseurl = await generate_job_search_url(job, page_number=1)
        logging.warning(f"Collecting data for {job} position")

        try:
            total_pages = await get_total_pages(baseurl, TOTAL_PAGE_SELECTOR)
            logging.info(f"Number of pages : {total_pages}")

            async with async_playwright() as p:
                browser = await p.chromium.launch()

                for page_number in range(1, total_pages + 1):
                    logging.warning(f"Collecting data for page {page_number}/{total_pages} for {job} position")
                    job_search_url = await generate_job_search_url(job, page_number)
                    page = await browser.new_page()
                    job_links = await extract_links(page, job_search_url, JOB_LINK_SELECTOR)

                    for i, link in enumerate(job_links, start=1):
                        logging.info(f'Scraping page {page_number} offer {i} for {job} position')
                        complete_url = f'{RACINE_URL}{link}'
                        html = await get_html(complete_url)
                        if html:
                            # Use a dictionary for each job offer
                            job_offer = {}

                            # Add contract_data, company_data, skill_categories, raw_description as sub-dictionaries
                            job_offer['source'] = "welcometothejungle"

                            contract_data = await get_contract_elements(html, CONTRACT_INFO_SELECTOR,
                                                                                     CONTRACT_SELECTORS)
                            for key, value in contract_data.items():
                                job_offer[key] = value

                            job_offer['company_data'] = await get_company_elements(html, COMPANY_INFO_SELECTOR,
                                                                                   COMPANY_SELECTORS)

                            job_offer['skills'] = await get_job_skills(html, JOB_DESCRIPTION_SELECTOR,
                                                                                 SKILLS_DICT)

                            job_offer['link'] = complete_url

                            job_offer['description'] = await get_raw_description(html, JOB_DESCRIPTION_SELECTOR)

                            all_job_offers.append(job_offer)

        except Exception as e:
            logging.error(f'Unexpected error : {e}')

    # Remove duplicate dictionaries from all_job_offers
    unique_job_offers = []
    seen_job_offers = set()
    for job_offer in all_job_offers:
        job_offer_tuple = tuple(sorted(job_offer.items()))  # Convert the dictionary to a tuple of sorted items
        if job_offer_tuple not in seen_job_offers:
            unique_job_offers.append(job_offer)
            seen_job_offers.add(job_offer_tuple)

    all_job_offers = unique_job_offers  # Replace all_job_offers with the unique list

    # Get the week number
    week_number = datetime.datetime.now().isocalendar()[1]
    # Save the output in a json file with the week number in the name
    save_file(all_job_offers, f'wttj_database_{week_number}.json')


if __name__ == "__main__":
    asyncio.run(main())
    sys.exit()