import openai

from os import environ
from dotenv import load_dotenv
from flask import Flask, request
from article_scraper import ArticleScraper
from open_ai import OpenAI
from typing import Dict


app = Flask(__name__)
load_dotenv()

openai.api_key = environ.get("OPENAI_API_KEY")


def get_summary(data: Dict[str, str]) -> Dict[str, str]:
    # Get data from request JSON
    data: dict[str, str] = request.json

    # Extract URL from data
    url: str = data['url']

    # Initialize article scraper with URL
    scraper: ArticleScraper = ArticleScraper(url)

    # Fetch article text and store it as a string
    text_to_summerize: str = scraper.fetch_data()

    # Initialize OpenAI instance with model and prompt
    open_ai: OpenAI = OpenAI("text-davinci-003",
                             f"Give me a summary of {text_to_summerize}", 0.8, 120)

    # Use OpenAI to summarize article text and store summary as a string
    summary: str = open_ai.summarize_text(text_to_summerize)

    # Return summary as JSON response
    return {
        "summary": summary
    }
