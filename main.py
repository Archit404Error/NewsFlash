from flask import Flask, request, render_template, jsonify
from cache_handler import cache_query, trending_news, top_news
import json
import requests

#FIXME: Change how outlets are displayed under article title
#TODO: Implement mobile client to query API

#Initialize server
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    return render_template("index.html", top_articles = top_news("top_cache.json"))

@app.route('/summaries', methods=['GET', 'POST'])
def summaries() -> str:
    #Store user topic from homepage post request
    topic = request.form['topic']
    topic = topic.replace(" ", "+")

    url = "http://localhost:5000/api?{}"
    api_res = requests.get(url.format(topic))
    res_json = api_res.json()

    topic = res_json["topic"]
    sources = res_json["sources"]
    outlet_summaries = res_json["summaries"]
    biases = res_json["biases"]
    article_links = res_json["articles"]
    sentiments = res_json["sentiments"]

    return render_template("summaries.html", topic = topic, sources = sources,
    outlet_summaries = outlet_summaries, biases = biases, article_links = article_links, sentiments = sentiments)

@app.route('/trending', methods=['GET', 'POST'])
def trending() -> str:
    trending_topics = trending_news('query_cache.json')
    return render_template("trending.html", trending_topics = trending_topics)

@app.route('/api')
def apiRes() -> str:
    #Store user topic from request
    topic = ""
    for item in request.args:
        topic = item
    sources, outlet_summaries, biases, article_links, sentiments = cache_query('query_cache.json', topic)

    return jsonify(topic = topic, articles = article_links, summaries = outlet_summaries, sources = sources, biases = biases, sentiments = sentiments)

if __name__ == "__main__":
    app.run(debug=True)
