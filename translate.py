import openai

from os import environ
from dotenv import load_dotenv
from flask import Flask, request
from open_ai import OpenAI


app = Flask(__name__)
load_dotenv()

openai.api_key = environ.get("OPENAI_API_KEY")


def translate_text(data: dict[str, str]) -> dict[str, str]:
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
    return {
        "translation": translated_text
    }
