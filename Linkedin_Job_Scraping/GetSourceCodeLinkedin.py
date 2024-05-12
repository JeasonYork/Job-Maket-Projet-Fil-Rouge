import requests
from bs4 import BeautifulSoup

url = 'https://www.linkedin.com/jobs/search/?currentJobId=3798762878&geoId=105080838&keywords=data%20engineer&location=New%20York%2C%20%C3%89tats-Unis&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true&'  # Replace with the URL of the web page you want to scrape

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the HTML content
    html_content = response.text

    # Save the HTML content to a file
    with open('LinkedInHTML.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print('HTML content saved to file.txt')
else:
    print(f'Error: {response.status_code}')
