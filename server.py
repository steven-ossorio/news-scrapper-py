import openai
import json

from os import environ
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from news_scraper import NewsScraper
from article_scraper import ArticleScraper
from textblob import TextBlob
from collections import defaultdict
from open_ai import OpenAI
from typing import List, Dict, Any


app = Flask(__name__)
load_dotenv()

openai.api_key = environ.get("OPENAI_API_KEY")


@app.route("/get_news", methods=["POST"])
def get_news() -> dict[str, Any]:
    # Get data from request JSON
    data: dict[str, str] = request.json

    # Extract source and topic from data
    source: str = data['source']
    article_topic: str = data['topic']

    # Construct URL from source and topic
    url: str = f"https://www.{source}.com/{article_topic}"

    # Initialize scraper with URL
    scraper: NewsScraper = NewsScraper(url)

    # Scrape news articles and store them in a list of dictionaries
    articles: List[Dict[str, str]] = json.loads(scraper.to_json())

    # Calculate sentiment scores for each article's title using TextBlob
    sentiment_scores: List[float] = [
        TextBlob(article['title']).sentiment.polarity for article in articles]

    # Calculate the average sentiment score for all articles
    average_sentiment_score: float = sum(
        sentiment_scores) / len(sentiment_scores)

    # Determine sentiment based on average sentiment score
    sentiment: str = "positive" if average_sentiment_score > 0 else "negative" if average_sentiment_score < 0 else "neutral"

    # Return articles and sentiment as JSON response
    return jsonify(
        {"articles": articles, "sentiment": sentiment}
    )


@app.route("/summary", methods=["POST"])
def get_summary() -> dict[str, str]:
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
    return jsonify({
        "summary": summary
    })


@app.route("/translate", methods=["POST"])
def translate_text() -> dict[str, str]:
    # Get data from request JSON
    data: dict[str, str] = request.json

    # Extract text and language from data
    text: str = data['text']
    language: str = data['language']

    # Initialize OpenAI instance with model and prompt
    open_ai: OpenAI = OpenAI("text-davinci-003",
                             f"Translate {text} to {language}", 0.2, 120)

    # Use OpenAI to translate text and store translated text as a string
    translated_text: str = open_ai.translate_text(text, language)

    # Return translated text as JSON response
    return jsonify({
        "translation": translated_text
    })


if __name__ == "__main__":
    app.run(debug=True)
