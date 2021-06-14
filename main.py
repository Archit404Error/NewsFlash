from flask import Flask, request, render_template, jsonify
from newsflash import collect_news
import json

#TODO: Extend caches to api page and reset cache daily
#TODO: Display most popular searches(perhaps replace trending page with this info)
#TODO: Use sentiment analysis on articles to show how each side feels
#TODO: Update Cache capabilities to support multiple cached lists

#Initialize server
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    return render_template("index.html")

@app.route('/summaries', methods=['GET', 'POST'])
def summaries() -> str:
    #Store user topic from homepage post request
    topic = request.form['topic']
    cache = open('cache.json', 'r+')

    if topic in cache.read():
        cache = open('cache.json', 'r+')
        converted_data = json.load(cache)
        sources = converted_data[1]
        outlet_summaries = converted_data[2]
        biases = converted_data[3]
        article_links = converted_data[4]
    else:
        sources, outlet_summaries, biases, article_links = collect_news(topic)
        json_data = [topic, sources, outlet_summaries, biases, article_links]
        json.dump(json_data, cache)

    return render_template("summaries.html", topic = topic, sources = sources,
    outlet_summaries = outlet_summaries, biases = biases, article_links = article_links)

@app.route('/trending', methods=['GET', 'POST'])
def trending() -> str:
    outlet_summaries = get_trending()
    return render_template("trending.html", outlet_summaries = outlet_summaries)

@app.route('/api')
def apiRes() -> str:
    #Store user topic from request
    topic = ""
    for item in request.args:
        topic = item
    print(topic)
    sources, outlet_summaries, biases, article_links = collect_news(topic)

    return jsonify(topic = topic, articles = article_links, summaries = outlet_summaries)

if __name__ == "__main__":
    app.run(debug=True)
