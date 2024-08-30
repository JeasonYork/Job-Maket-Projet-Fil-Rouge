"""
This module groups together all the functions needed to obtain information from web pages.
"""

import asyncio
import logging

# Configuration du journal dans un fichier
logger = logging.getLogger("scrap_wttj.data_extraction")


async def extract_links(page, job_search_url: str, job_links_selector: str):
    """
    Function that extracts all links to offers from each search page
    :param page: instance of the page via Playwright
    :param job_search_url: url of search pages
    :param job_links_selector: selector of the tag where the information is found
    :return: list of links
    """
    try:
        await page.goto(job_search_url, timeout=15000)
        await page.wait_for_load_state("networkidle")
        logging.info(f"Navigated to {job_search_url}")

        await page.wait_for_selector(job_links_selector, timeout=15000)
        logging.info(f"Found job links selector: {job_links_selector}")

        elements = await page.query_selector_all(job_links_selector)
        links = [await element.get_attribute("href") for element in elements]
        logging.info(f"Extracted links: {links}")

        return links
    except Exception as e:
        logging.error(f"Error extracting links: {str(e)}")
        return []


def get_info(html, selector, parent=True):
    """
    Function that extracts and formats all the information you need from job details pages.
    :param html: HTML code of the page to be scrapped
    :param selector: scraper information selector
    :param parent: For some tags, we had to use sub-tags because the generic tag was repeated in several places in the
    code. We then retrieve the parent tag to extract the information, as the desired information may lie outside the
    indentifiable tags.
    :return str: Text containing information
    """
    replacements = {
        "Salaire : ": "",
        "Expérience : ": "",
        "Éducation : ": "",
        " collaborateurs": "",
        "Créée en ": "",
        "Âge moyen : ": "",
        " ans": "",
        "Chiffre d'affaires : ": "",
        "M€": "",
        "%": "",
        "&nbsp;": " ",
        "&NBSP;": " ",
    }

    try:
        text = (
            html.css_first(selector).parent.text()
            if parent
            else html.css_first(selector).text()
        )
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text
    except AttributeError:
        return None


async def get_contract_elements(html, contract_info_selector, CONTRACT_SELECTORS):
    """
    Function that extracts contract elements from HTML and return the extracted data.
    :param html: HTML code of the page we want to scrape
    :param contract_info_selector: selector that contains all the information related to contract details
    :param CONTRACT_SELECTORS: list selector to scrape each element
    :return: elements relative to the job
    """
    contract_elements = html.css_first(contract_info_selector)

    try:
        job_title = get_info(
            contract_elements, CONTRACT_SELECTORS["job_title"], parent=False
        )
        contract_type = get_info(contract_elements, CONTRACT_SELECTORS["contract_type"])
        salary = get_info(contract_elements, CONTRACT_SELECTORS["salary"])
        company = get_info(
            contract_elements, CONTRACT_SELECTORS["company"], parent=False
        )
        location = get_info(contract_elements, CONTRACT_SELECTORS["location"])
        remote = get_info(contract_elements, CONTRACT_SELECTORS["remote"])
        experience = get_info(contract_elements, CONTRACT_SELECTORS["experience"])
        education_level = get_info(
            contract_elements, CONTRACT_SELECTORS["education_level"]
        )

        time_element = contract_elements.css_first("time")
        publication_date = (
            time_element.attributes["datetime"][0:10] if time_element else None
        )

        contract_data = {
            "job_title": job_title,
            "contract_type": contract_type,
            "salary": salary,
            "company": company,
            "location": location,
            "remote": remote,
            "experience": experience,
            "education_level": education_level,
            "publication_date": publication_date,
        }

        return contract_data
    except Exception as e:
        logging.error(f"Error during extraction of contract elements: {e}")
        raise


async def get_company_elements(html, company_info_selector, COMPANY_SELECTORS):
    """
    Function that extracts company elements from HTML and return the extracted data.
    :param html: HTML code of the page we want to scrape
    :param company_info_selector: selector that contains all the information related to company details
    :param COMPANY_SELECTORS: list selector to scrape each element
    :return: elements relative to the company
    """
    try:
        company_elements = html.css_first(company_info_selector)

        sector = get_info(company_elements, COMPANY_SELECTORS["sector"])
        company_size = get_info(company_elements, COMPANY_SELECTORS["company_size"])
        turnover_in_millions = get_info(
            company_elements, COMPANY_SELECTORS["turnover_in_millions"]
        )

        company_data = {
            "sector": sector,
            "company_size": company_size,
            "turnover_in_millions": turnover_in_millions,
        }
        return company_data

    except Exception as e:
        logging.error(f"Error during extraction of company elements: {e}")
        raise


async def get_raw_description(html, selector):
    try:
        raw_description = html.css_first(selector)
        if raw_description:
            return raw_description.text()
        else:
            return None
    except Exception as e:
        logging.error(f"An error occurred while parsing HTML: {e}")
        return None
