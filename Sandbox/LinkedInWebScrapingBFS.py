import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import time

l = []
o = {}
k = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

# URL of the LinkedIn job search results page
target_url = 'https://www.linkedin.com/jobs/search/?currentJobId=3798762878&geoId=105080838&keywords=data%20engineer&location=New%20York%2C%20%C3%89tats-Unis&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true&'

response = requests.get(target_url)
soup = BeautifulSoup(response.text, 'html.parser')

print(f"Error: {response.status_code}")

# Check if the request was successful
if response.status_code == 200:
    # Get the HTML content
    html_content = response.text

    # Save the HTML content to a file
    '''
    with open('LinkedInHTML.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    '''
    # Locate the div containing the number of results
    #results_div = soup.find('div', class_='jobs-search-results-list__subtitle')
    # Extract the text content
    #results_text = results_div.find('span').get_text(strip=True)
    # Extract only the numeric part
    #numeric_results = ''.join(c for c in results_text if c.isdigit())
    numeric_results  = 703
    delay_seconds = 0.5 

    for i in range(0, math.ceil(numeric_results / 25)):

        res = requests.get(target_url.format(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all("li")
        print(len(alljobs_on_this_page))
        for x in range(0, len(alljobs_on_this_page)):
            job_list = alljobs_on_this_page[x].find("div", {"class": "jobs-search__results-list"}) 
            if job_list:
                base_card = job_list.find("div", {"class": "base-card"})

                if base_card:
                    data_entity_urn = base_card.get('data-entity-urn')

                    if data_entity_urn:
                        jobid = data_entity_urn.split(":")[3]
                        l.append(jobid)

                        # Check if 'sr-only' class exists within the base_card
                        sr_only_spans = base_card.find_all('span', class_='sr-only')

                        if sr_only_spans:
                            # Extract the text content from each span
                            for span in sr_only_spans:
                                job_title = span.get_text(strip=True)
                                print(f"Job Title: {job_title}")
                        else:
                            print("Error: 'sr-only' class not found in base_card.")
                    else:
                        print("Error: 'data-entity-urn' attribute not found for base-card.")
                else:
                    print("Error: 'base-card' div not found in alljobs_on_this_page.")
            else:
                    print("Error: 'jobs-search__results-list' div not found.")
            time.sleep(delay_seconds)

    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(0, len(l)):

        resp = requests.get(target_url.format(l[j]))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            o["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            o["company"] = None

        try:
            o["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            o["job-title"] = None

        try:
            o["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace(
                "Seniority level", "").strip()
        except:
            o["level"] = None
        time.sleep(delay_seconds)

        k.append(o)
        o = {}

    df = pd.DataFrame(k)
    df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')
    print(k)

    print(f"Number of Results: {numeric_results}")

else:
    print(f"Error: {response.status_code}")
