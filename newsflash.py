from content_categorizer import classify_topic
from news_scraper import get_news, get_trending
from summary import summarize_text

#List of business sources
business_sources = ['australian-financial-review', 'bloomberg', 'business-insider', 'financial-post', 'fortune', 'the-wall-street-journal']

#List of tech sources
tech_sources = ['ars-technica', 'engadget', 'hacker-news', 'recode', 'techcrunch', 'techradar', 'the-next-web', 'wired']

#List of science sources
science_sources = ['national-geographic', 'new-scientist', 'next-big-future']

#List of sports sources
sports_sources = ['espn', 'bleacher-report', 'four-four-two', 'nfl-news', 'nhl-news', 'talksport', 'the-sport-bible', 'bbc-sport']

#List of political sources
political_sources = ['bbc-news', 'cnn', 'fox-news', 'abc-news', 'breitbart-news', 'axios', 'the-hill', 'the-washington-post']

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
                         "Game" : sports_sources,
                         "Sports" : sports_sources,
                         "Society" : political_sources,
                         "Health" : political_sources
                       }

def collect_news(topic):
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

    return sources, outlet_summaries, biases, article_links
