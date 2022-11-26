import json

import requests
from flask import Flask, jsonify, render_template, request

from cache_handler import cache_query, clear_caches, top_news, trending_news
from newsflash import analyze_article

#Initialize server
app = Flask(__name__)

def get_news(topic):
    parsed_articles, sentiments = cache_query('query_cache.json', topic)

    return jsonify(topic = topic, parsed_articles = parsed_articles, sentiments = sentiments)

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    top_articles = topRes().json["top_articles"]
    return render_template("index.html", top_articles = top_articles)

@app.route('/mobile')
def mobile() -> str:
    return render_template("mobile.html")

@app.route('/summaries', methods=['GET', 'POST'])
def summaries() -> str:
    #Store user topic from homepage post request
    topic = request.form['topic']
    topic = topic.title()
    topic = topic.replace(" ", "+")

    res_json =  get_news(topic).json

    topic = res_json["topic"]
    parsed_articles = res_json["parsed_articles"]
    sentiments = res_json["sentiments"]

    return render_template("summaries.html", topic = topic, parsed_articles = parsed_articles, sentiments = sentiments)

@app.route('/trending', methods=['GET', 'POST'])
def trending() -> str:
    trending_topics = trendingApi().json["trending_list"]
    return render_template("trending.html", trending_topics = trending_topics)

@app.route('/api')
def apiRes() -> str:
    #Store user topic from request
    topic = list(request.args)[0]
    return get_news(topic)

@app.route('/topApi')
def topRes() -> str:
    return jsonify(top_articles = top_news("top_cache.json"))

@app.route('/analysisApi')
def articleAnalysis() -> str:
    article_url = list(request.args)[0]

    title, image, keywords, summary, sentiment_list = analyze_article(article_url, nlp = True)
    return jsonify(title = title, image = image, keywords = keywords, summary = summary, sentiment = sentiment_list)

@app.route('/trendingApi')
def trendingApi() -> str:
    return jsonify(trending_list = trending_news('query_cache.json'))

@app.route('/fullArticle')
def fullApi() -> str:
    article_url = list(request.args)[0]
    title, image, full_text = analyze_article(article_url, nlp = False)
    return jsonify(title = title, image = image, full_text = full_text)

@app.route('/reset')
def clear() -> str:
    clear_caches(['query_cache.json', 'top_cache.json'])

@app.route('/privacy')
def privacy() -> str:
    return render_template('privacy.html')

@app.route('/support')
def contact() -> str:
    return render_template('support.html')

if __name__ == "__main__":
    app.run(debug=True)
