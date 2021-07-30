from flask import Flask, request, render_template, jsonify
from cache_handler import cache_query, trending_news, top_news, clear_caches
from newsflash import analyze_article
import json
import requests

#FIXME: Change how outlets are displayed under article title
#TODO: Implement mobile client to query API

#Initialize server
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    url = "http://news-flash-proj.herokuapp.com/topApi"
    top_res = requests.get(url)
    top_articles = top_res.json()["top_articles"]
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

    url = "http://news-flash-proj.herokuapp.com/api?{}"
    api_res = requests.get(url.format(topic))
    res_json = api_res.json()

    topic = res_json["topic"]
    parsed_articles = res_json["parsed_articles"]
    sentiments = res_json["sentiments"]

    return render_template("summaries.html", topic = topic, parsed_articles = parsed_articles, sentiments = sentiments)

@app.route('/trending', methods=['GET', 'POST'])
def trending() -> str:
    trending_url = "http://news-flash-proj.herokuapp.com/trendingApi"
    trending_topics = requests.get(trending_url).json()["trending_list"]
    return render_template("trending.html", trending_topics = trending_topics)

@app.route('/api')
def apiRes() -> str:
    #Store user topic from request
    topic = list(request.args)[0]
    parsed_articles, sentiments = cache_query('query_cache.json', topic)

    return jsonify(topic = topic, parsed_articles = parsed_articles, sentiments = sentiments)

@app.route('/topApi')
def topRes() -> str:
    return jsonify(top_articles = top_news("top_cache.json"))

@app.route('/analysisApi')
def articleAnalysis() -> str:
    article_url = list(request.args)[0]

    title, image, keywords, summary, sentiment_list = analyze_article(article_url)
    return jsonify(title = title, image = image, keywords = keywords, summary = summary, sentiment = sentiment_list)

@app.route('/trendingApi')
def trendingApi() -> str:
    return jsonify(trending_list = trending_news('query_cache.json'))

@app.route('/reset')
def clear() -> str:
    clear_caches(['query_cache.json', 'top_cache.json'])

@app.route('/privacy')
def privacy() -> str:
    return render_template('privacy.html')

if __name__ == "__main__":
    app.run(debug=True)
