import json

from flask import request
from news_scraper import NewsScraper
from textblob import TextBlob
from typing import List, Dict, Any


def get_news(data: Dict[str, str]) -> Dict[str, Any]:
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
    return {"articles": articles, "sentiment": sentiment}
