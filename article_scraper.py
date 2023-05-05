import requests
from bs4 import BeautifulSoup


class ArticleScraper:
    """
    A class for scraping article text from a given URL.

    Attributes:
        url (str): The URL to scrape data from.
        headers (dict): The HTTP headers to use when making requests.
    """

    def __init__(self, url: str) -> None:
        """
        Initialize the ArticleScraper with a URL and User-Agent header.

        Args:
            url (str): The URL to scrape data from.
        """

        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_data(self) -> str:
        """
        Scrape the article text from the URL using BeautifulSoup.

        Returns: 
            string: A string containing the article text.
        """

        request = requests.get(self.url, headers=self.headers)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser')

        texts = soup.find_all('p')
        paragraph = ""
        for text in texts:
            text = text.text.strip()
            if len(paragraph) > 1400:
                print("breaking")
                break
            paragraph += text + " "

        return paragraph
