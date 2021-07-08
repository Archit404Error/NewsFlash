from content_categorizer import classify_topic, sentiment_analysis
from news_scraper import get_news
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
                         "Health" : political_sources,
                         "Games" : political_sources,
                         "Arts" : political_sources,
                         "Home" : political_sources
                       }

def collect_news(topic):
    #Use classification function and store result
    topic_category = classify_topic(topic)

    #Format topic for api query
    topic = topic.replace(" ", "+")

    #Determine source list based upon categorization
    sources = category_to_list_map[topic_category]
    source_dict = {}
    for source in sources:
        source_dict[source] = False

    parsed_articles = get_news(source_dict, topic)

    full_texts = {}
    for source_id, parsed_arr in parsed_articles.items():
        article_text = parsed_arr[2]
        full_texts[source_id] = article_text
        if source_id in biases.keys():
            bias = biases[source_id]
        else:
            bias = "centrist"
        parsed_articles[source_id] = [parsed_arr[0], parsed_arr[1], summarize_text(article_text), bias]

    sentiments = sentiment_analysis(full_texts)
    return parsed_articles, sentiments
