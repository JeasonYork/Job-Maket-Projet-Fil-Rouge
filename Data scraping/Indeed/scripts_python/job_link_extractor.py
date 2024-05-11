from playwright.async_api import async_playwright
import asyncio
import re
import logging
import random
import sys
from pathlib import Path

######################## CONSTANTS ########################
# Use of regular expression to identify all the links we're looking for (used in extract_links)
LIST_OF_POSITIONS = [
    "data engineer",
    "data architect",
    "data scientist",
    "data analyst",
    "software engineer",
    "Data Warehousing Engineer",
    "Machine Learning Engineer",
    "cloud architect",
    "solution architect",
    "cloud engineer",
    "big data engineer",
    "Data Infrastructure Engineer",
    "Data Pipeline Engineer",
    "ETL Developer",
]
TYPE_OF_CONTRACT = [
    "permanent",
    "fulltime",
    "internship",
    "contract",
    "subcontract",
    "apprenticeship",
    "custom_1",
    "temporary",
    "parttime",
]
RACINE_URL = ["https://fr.indeed.com/jobs?q=", "&sc=0kf%3Ajt%28", "%29%3B"]
JOB_LINKS_PATTERN = re.compile(r"\b\w*(/pagead/clk?|/rc/clk?)\w*\b")
NEXT_PAGE_SELECTOR = '[data-testid="pagination-page-next"]'


#################### Enregistrement csv #######################
data_directory = Path.joinpath(Path(__file__).parent, "data")
txt_filename = "job_links.txt"
txt_path = Path.joinpath(data_directory, txt_filename)


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler("logfile_joblinks.txt"),
    ],
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()
logger.handlers[0].setLevel(logging.INFO)


async def extract_links(url, page, pattern):
    try:
        for attemp in range(3):
            await page.goto(url)
            await asyncio.sleep(random.uniform(0.5, 1))
            await page.wait_for_load_state("networkidle")

            await asyncio.sleep(random.uniform(0.5, 1))

            all_links = await page.evaluate(
                """() => {
                const linksInSliderContainer = Array.from(document.querySelectorAll('div.slider_container a'));
                return linksInSliderContainer.map(a => a.href);
            }"""
            )

            links = [link for link in all_links if re.search(pattern, link)]

            await asyncio.sleep(random.uniform(0.5, 1))

            logging.info(f"Number of links extracted: {len(links)}")
            return links

    except Exception as e:
        logging.error(f"Error extracting links: {e}")
        pass


async def get_next_page_link(page, next_page_selector, job_position):
    try:
        for attemp in range(3):
            links = await page.query_selector_all(next_page_selector)

            await asyncio.sleep(random.uniform(0.5, 1))

            regex_pattern = rf"^https:\/\/fr\.indeed\.com\/jobs\?q={job_position.replace(' ', r'\+')}"

            next_page_link = await page.evaluate(
                r"(links) => {"
                + fr"   const regex = /{regex_pattern}/;"
                + r"    const filteredLinks = Array.from(links, link => link.href).find("
                + r"        href => regex.test(href)"
                + r"    );"
                + r"    return filteredLinks;"
                + r"}",
                links,
                )

            return next_page_link

    except Exception as e:
        logging.error(f"Error extracting next page link: {e}")
        return None


# Function to save links to a file
async def save_links_to_file(liste, directory, file_path):
    if not data_directory.exists():
        data_directory.mkdir(parents=True)

    else :
        with open(file_path, "a", encoding="utf-8") as file:
            for link in liste:
                file.write(link + "\n")



async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)

        context = await browser.new_context()

        page = await context.new_page()

        all_jobs_links = []

        for job_position in LIST_OF_POSITIONS:
            for type_contract in TYPE_OF_CONTRACT:
                base_url = f"{RACINE_URL[0]}{job_position.replace(" ", "+")}{RACINE_URL[1]}{type_contract}{RACINE_URL[2]}"

                await page.goto(base_url)

                await asyncio.sleep(5)

                for attempt in range(3):
                    try:
                        await page.wait_for_load_state("networkidle")
                        break
                    except TimeoutError:
                        logging.warning("Timeout waiting for network idle state.")
                while True:
                    job_links = await extract_links(base_url, page, JOB_LINKS_PATTERN)

                    if job_links is not None:
                        all_jobs_links.extend(job_links)
                        await save_links_to_file(job_links, data_directory, txt_path)
                        logger.info(f"Saved links from page {base_url}")
                    else:
                        logger.warning(f"No links extracted from page {base_url}")
                        pass

                    await asyncio.sleep(random.uniform(0.5, 1))

                    next_page_link = await get_next_page_link(page, NEXT_PAGE_SELECTOR, job_position)

                    if not next_page_link or next_page_link is None:
                        break

                    base_url = next_page_link

                    await page.goto(next_page_link)
                    await asyncio.sleep(random.uniform(0.5, 1))
                    await page.wait_for_load_state("networkidle")
                    logging.info(f"Following link found: {next_page_link}")

        await asyncio.sleep(2)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
