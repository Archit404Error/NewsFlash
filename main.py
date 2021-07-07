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

    url = "http://news-flash-proj.herokuapp.com/api?{}"
    api_res = requests.get(url.format(topic))
    res_json = api_res.json()

    topic = res_json["topic"]
    parsed_articles = res_json["parsed_articles"]
    sentiments = res_json["sentiments"]

    return render_template("summaries.html", topic = topic, parsed_articles = parsed_articles, sentiments = sentiments)

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
    parsed_articles, sentiments = cache_query('query_cache.json', topic)

    return jsonify(topic = topic, parsed_articles = parsed_articles, sentiments = sentiments)

if __name__ == "__main__":
    app.run(debug=True)
