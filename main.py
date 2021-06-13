from flask import Flask, request, render_template, jsonify
from newsflash import collect_news

#TODO: Cache queries to reduce total API requests made
#TODO: Display most popular searches(perhaps replace trending page with this info)
#TODO: Use sentiment analysis on articles to show how each side feels

#Initialize server
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    return render_template("index.html")

@app.route('/summaries', methods=['GET', 'POST'])
def summaries() -> str:
    #Store user topic from homepage post request
    topic = request.form['topic']

    sources, outlet_summaries, biases, article_links = collect_news(topic)

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
