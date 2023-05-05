from flask import Flask, request, jsonify
from news import get_news
from summary import get_summary
from translate import translate_text

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/news', methods=['POST'])
def news():
    return jsonify(get_news(request.json))


@app.route('/summary', methods=['POST'])
def summary():
    return jsonify(get_summary(request.json))


@app.route('/translate', methods=['POST'])
def translate():
    return jsonify(translate_text(request.json))


if __name__ == '__main__':
    app.run()
