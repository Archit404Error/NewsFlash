from flask import Flask, request, render_template
from content_categorizer import classify_topic
from news_scraper import get_news, get_trending
from summary import summarize_text

#TODO: Cache queries to reduce total API requests made
#TODO: Display most popular searches(perhaps replace trending page with this info)

#Initialize server
app = Flask(__name__)

#List of business sources
business_sources = ['australian-financial-review', 'bloomberg', 'business-insider',
        'financial-post']

#List of tech sources
tech_sources = ['engadget', 'hacker-news', 'recode']

#List of science sources
science_sources = ['national-geographic', 'new-scientist', 'next-big-future']

#List of sports sources
sports_sources = ['espn', 'bleacher-report', 'four-four-two']

#List of political sources
political_sources = ['bbc-news', 'cnn', 'fox-news', 'abc-news', 'breitbart-news', 'axios',
            'the-hill', 'the-washington-post']

#Dictionary of politcial affiliation by source
biases = {'bbc-news' : 'center', 'cnn' : 'liberal', 'fox-news' : 'conservative',
            'abc-news' : 'liberal', 'breitbart-news' : 'conservative',
            'axios' : 'center', 'the-hill' : 'center',
            'the-washington-post' : 'liberal'}

#Create map to find list based on categorization(since Python doesn't have switch statements)
category_to_list_map = {
                         "Business" : business_sources,
                         "Computers" : tech_sources,
                         "Science" : science_sources,
                         "Sports" : sports_sources,
                         "Society" : political_sources
                       }

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

    #Format topic for api query
    topic = topic.replace(" ", "+")

    #Determine source list based upon categorization
    sources = category_to_list_map[topic_category]

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
