import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class NewsScraper:
    """
    A class for scraping news articles from various domains.

    Attributes:
        url (str): The URL to scrape data from.
        headers (dict): The HTTP headers to use when making requests.
        accepted_domains (dict): A dictionary mapping supported domains to their corresponding scraping methods.
    """

    def __init__(self, url):
        """
        Initializes a NewsScraper object with the given URL.

        Args:
            url (str): The URL to scrape data from.
        """
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.accepted_domains = {
            "https://www.skysports.com": self.skyports,
            "https://www.cnn.com": self.cnn,
        }

    def fetch_data(self):
        """
        Fetches the data from the specified URL and returns it as a list of dictionaries.

        Returns:
            list: A list of dictionaries, with each dictionary containing the title and link of an article.
        """
        request = requests.get(self.url, headers=self.headers)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')

        parsed_url = urlparse(self.url)

        domain = parsed_url.scheme + "://" + parsed_url.netloc

        if domain not in self.accepted_domains:
            raise ValueError(f"Unsupported domain: {domain}")

        data = self.accepted_domains[domain](soup, domain)
        return data

    def skyports(self, soup, _):
        """
        Scrapes news articles from Sky Sports.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML of the page.
            _ (str): Unused parameter.

        Returns:
            list: A list of dictionaries, with each dictionary containing the title and link of an article.
        """
        articles = soup.find_all('a', class_=[
            'news-list__headline-link',
        ])

        data = []
        for article in articles:
            link = article.get('href')
            title = article.text.strip()
            data.append({'title': title, 'link': link})

        return data

    def cnn(self, soup, domain):
        """
        Scrapes news articles from CNN.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML of the page.
            domain (str): The domain of the page.

        Returns:
            list: A list of dictionaries, with each dictionary containing the title and link of an article.
        """
        articles = soup.find_all('a', class_='container__link')

        data = []
        for article in articles:
            link = article.get('href')
            link = domain + link

            title_div = article.find('div', class_='container__text')
            if title_div:
                title_span = title_div.find('div').find(
                    'span', {'data-editable': 'headline'})
                if title_span:
                    title = title_span.text.strip()

                    data.append({'title': title, 'link': link})
        return data

    def to_json(self):
        """
        Fetches the data from the specified URL and returns it as a JSON string.

        Returns:
            str: A JSON string representing the scraped data.
        """
        data = self.fetch_data()
        return json.dumps(data)
