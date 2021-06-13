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
        'financial-post', 'fortune', 'the-wall-street-journal']

#List of tech sources
tech_sources = ['ars-technica', 'engadget', 'hacker-news', 'recode', 'techcrunch',
        'techradar', 'the-next-web', 'wired']

#List of science sources
science_sources = ['national-geographic', 'new-scientist', 'next-big-future']

#List of sports sources
sports_sources = ['espn', 'bleacher-report', 'four-four-two', 'nfl-news', 'nhl-news',
        'talksport', 'the-sport-bible', 'bbc-sport']

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
                         "Society" : political_sources,
                         "Health" : political_sources
                       }

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    return render_template("index.html")

@app.route('/summaries', methods=['GET', 'POST'])
def summaries() -> str:
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
        #Summarize article text to enable faster reading
        outlet_summaries[source] = summarize_text(full_text)
        #Create key value pair in dictionary using source and link
        article_links[source] = article_link
    return render_template("summaries.html", topic = topic, sources = sources,
    outlet_summaries = outlet_summaries, biases = biases, article_links = article_links)

@app.route('/trending', methods=['GET', 'POST'])
def trending() -> str:
    outlet_summaries = get_trending()
    return render_template("trending.html", outlet_summaries = outlet_summaries)

if __name__ == "__main__":
    app.run(debug=True)
