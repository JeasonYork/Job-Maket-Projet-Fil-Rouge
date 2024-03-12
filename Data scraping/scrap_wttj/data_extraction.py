"""
This module groups together all the functions needed to obtain information from web pages.
"""
import logging
from selectolax.parser import HTMLParser


# Configuration des logs
logging.basicConfig(level=logging.INFO)

async def extract_links(page, job_search_url: str, job_links_selector: str):
    """
    Function that extracts all links to offers from each search page
    :param page: instance of the page via Playwright
    :param job_search_url: url of search pages
    :param job_links_selector: selector of the tag where the information is found
    :return: list of links
    """
    try:
        await page.goto(job_search_url, timeout=5000)

        # Wait until the page has loaded the content with the total number of pages
        await page.wait_for_selector(job_links_selector, timeout=5000)

        # Selection of all elements corresponding to the selector
        elements = await page.query_selector_all(job_links_selector)

        # Extract links using the get_attribute command
        links = [await element.get_attribute("href") for element in elements]

        return links
    except Exception as e:
        logging.error(f'Error extracting links: {str(e)}')
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
        "Salaire : ": "", "Expérience : ": "", "Éducation : ": "", " collaborateurs": "", "Créée en ": "",
        "Âge moyen : ": "", " ans": "", "Chiffre d'affaires : ": "", "M€": "", "%": "", "&nbsp;": " ", "&NBSP;": " "
    }

    try:
        text = html.css_first(selector).parent.text() if parent else html.css_first(selector).text()
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
    # Targeting my tag containing all basic data for the offer
    contract_elements = html.css_first(contract_info_selector)

    try:
        job_title = get_info(contract_elements, CONTRACT_SELECTORS['job_title'], parent=False)
        contract_type = get_info(contract_elements, CONTRACT_SELECTORS['contract_type'])
        salary = get_info(contract_elements, CONTRACT_SELECTORS['salary'])
        company = get_info(contract_elements, CONTRACT_SELECTORS['company'], parent=False)
        location = get_info(contract_elements, CONTRACT_SELECTORS['location'])
        remote = get_info(contract_elements, CONTRACT_SELECTORS['remote'])
        experience = get_info(contract_elements, CONTRACT_SELECTORS['experience'])
        education_level = get_info(contract_elements, CONTRACT_SELECTORS['education_level'])

        # Check if 'time' exists in contract_elements before accessing 'attributes' attribute
        # for publication_date the information appears directly in the tag .attributes
        time_element = contract_elements.css_first('time')
        publication_date = time_element.attributes['datetime'][0:10] if time_element else None

        contract_data = {
            'job_title': job_title, 'contract_type': contract_type, 'salary': salary, 'company': company,
            'location': location,
            'remote': remote, 'experience': experience, 'education_level': education_level,
            'publication_date': publication_date
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

        sector = get_info(company_elements, COMPANY_SELECTORS['sector'])
        company_size = get_info(company_elements, COMPANY_SELECTORS['company_size'])
        creation_date = get_info(company_elements, COMPANY_SELECTORS['creation_date'])
        # Check if address is None before applying split()
        address_info = get_info(company_elements, COMPANY_SELECTORS['address'], parent=False)
        address = ", ".join(address_info.split(", ")[:2]) if address_info else None
        average_age_of_employees = get_info(company_elements, COMPANY_SELECTORS['average_age_of_employees'])
        turnover_in_millions = get_info(company_elements, COMPANY_SELECTORS['turnover_in_millions'])
        proportion_female = get_info(company_elements, COMPANY_SELECTORS['proportion_female'])
        proportion_male = get_info(company_elements, COMPANY_SELECTORS['proportion_male'])

        company_data = {
            'sector': sector, 'company_size': company_size,
            'creation_date': creation_date, 'address': address, 'average_age_of_employees': average_age_of_employees,
            'turnover_in_millions': turnover_in_millions, 'proportion_female': proportion_female,
            'proportion_male': proportion_male
        }
        return company_data

    except Exception as e:
        logging.error(f"Error during extraction of company elements: {e}")
        raise


async def get_job_skills(html, job_description_selector, job_info_dict):


    try:
        # Utiliser html.css_first() pour extraire le contenu du sélecteur CSS
        job_description_element = html.css_first(job_description_selector)

        # Vérifier si l'élément existe
        if job_description_element:
            # Obtenir le texte de la description du travail
            job_description = job_description_element.text()

            # Dictionnaire pour stocker les résultats
            result_dict = {}

            # Parcourir le dictionnaire des compétences
            for skill, keywords in job_info_dict.items():
                # Liste pour stocker les résultats pour chaque compétence
                skill_results = []

                # Parcourir les mots-clés de la compétence
                for keyword in keywords:
                    # Vérifier si le mot-clé est présent dans la description du travail
                    if keyword.lower() in job_description.lower():
                        # Si présent, ajouter à la liste des compétences
                        skill_results.extend(
                            [word.lower() for word in job_description.split() if keyword.lower() in word.lower()])

                # Ajouter les résultats au dictionnaire
                result_dict[skill] = skill_results if skill_results else None

            return result_dict
        else:
            logging.warning("Aucun élément trouvé avec le sélecteur CSS.")
            return None

    except Exception as e:
        # Gérer les exceptions et enregistrer les logs
        logging.error(f"Une erreur s'est produite: {str(e)}")
        return None


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
