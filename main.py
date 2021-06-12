from flask import Flask, request, render_template
from content_categorizer import classify_topic
from news_scraper import get_news, get_trending
from summary import summarize_text

#Initialize server
app = Flask(__name__)

#TODO: implement news sources by category (society, science, tech, etc.)
#List of news sources
sources = ['bbc-news', 'cnn', 'fox-news', 'abc-news', 'breitbart-news', 'axios',
            'the-hill', 'the-washington-post']

#Dictionary of politcial affiliation by source
biases = {'bbc-news' : 'center', 'cnn' : 'liberal', 'fox-news' : 'conservative',
            'abc-news' : 'liberal', 'breitbart-news' : 'conservative',
            'axios' : 'center', 'the-hill' : 'center',
            'the-washington-post' : 'liberal'}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/summaries', methods=['GET', 'POST'])
def summaries():
    #Store user topic from homepage post request
    topic = request.form['topic']

    #Initialize summaries and article links dictionaries
    outlet_summaries = {}
    article_links = {}

    #Use classification function and store result
    topic_category = classify_topic(topic)

    #format topic for api query
    topic = topic.replace(" ", "+")

    #TODO: Determine which source list to use in loop based on classification
    for source in sources:
        article_link, full_text = get_news(source, topic)
        outlet_summaries[source] = summarize_text(full_text)
        article_links[source] = article_link
    return render_template("summaries.html", topic = topic, sources = sources,
    outlet_summaries = outlet_summaries, biases = biases, article_links = article_links)

@app.route('/trending', methods=['GET', 'POST'])
def trending():
    outlet_summaries = get_trending()
    return render_template("trending.html", outlet_summaries = outlet_summaries)

if __name__ == "__main__":
    app.run(debug=True)
