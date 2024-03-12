import sys
from pathlib import Path

# Add the path of the parent directory to sys.path using pathlib
current_dir = Path('/Users/MoG/PycharmProjects/jobmarket/jobmarket')
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


async def generate_job_search_url(job, page_number):
    return f"https://www.welcometothejungle.com/fr/jobs?query={job.replace(" ", "%20")}&page={page_number}&aroundQuery=worldwide"


async def main():
    for job in JOBS:
        baseurl = await generate_job_search_url(job, page_number=1)
        logging.info(f"Switching to job : {job}")

        try:
            total_pages = await get_total_pages(baseurl, TOTAL_PAGE_SELECTOR)
            logging.info(f"Number of pages : {total_pages}")

            async with async_playwright() as p:
                browser = await p.chromium.launch()

                for page_number in range(1, total_pages + 1):
                    job_search_url = await generate_job_search_url(job, page_number)
                    page = await browser.new_page()
                    job_links = await extract_links(page, job_search_url, JOB_LINK_SELECTOR)

                    for i, link in enumerate(job_links, start=1):
                        print(f'Scraping page {page_number} offer {i}')
                        complete_url = f'{RACINE_URL}{link}'
                        html = await get_html(complete_url)
                        if html:
                            # Use a dictionary for each job offer
                            contract_data = await get_contract_elements(html, CONTRACT_INFO_SELECTOR,
                                                                        CONTRACT_SELECTORS)
                            company_data = await get_company_elements(html, COMPANY_INFO_SELECTOR, COMPANY_SELECTORS)

                            skills_data = await get_job_skills(html, JOB_DESCRIPTION_SELECTOR, SKILLS_DICT)

                            raw_description = await get_raw_description(html, JOB_DESCRIPTION_SELECTOR)

                            # Merge contract_data and company_data into a single dictionary
                            job_offer = {**contract_data, **company_data, **skills_data,
                                         'raw_description': raw_description}

                            # Save the output in a json file
                            save_file(job_offer, 'wttj_database_bronze')

        except Exception as e:
            logging.error(f'Erreur inattendue : {e}')


if __name__ == "__main__":
    asyncio.run(main())
    sys.exit()
