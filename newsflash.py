from newspaper import *
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
political_sources = ['bbc-news', 'cnn', 'fox-news', 'abc-news', 'breitbart-news', 'axios', 'the-hill', 'msnbc']

#Dictionary of politcial affiliation by source
biases = {'bbc-news' : 'center', 'cnn' : 'liberal', 'fox-news' : 'conservative',
            'abc-news' : 'liberal', 'breitbart-news' : 'conservative',
            'axios' : 'center', 'the-hill' : 'center',
            'msnbc' : 'liberal'}

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
                         "Home" : political_sources,
                         "Recreation" : sports_sources,
                       }

def collect_news(topic):
    #Use classification function and store result
    topic_category = classify_topic({"user-query" : topic})
    topic_category = topic_category["user-query"]

    #Format topic for api query
    topic = topic.replace(" ", "+")

    #Determine source list based upon categorization
    sources = category_to_list_map[topic_category]
    source_dict = {}
    for source in sources:
        source_dict[source] = False

    parsed_articles = get_news(source_dict, topic)

    if 'No Source Found' in parsed_articles.keys():
        source_dict = {}
        sources = category_to_list_map["Society"]
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

        summary = summarize_text(article_text)

        if parsed_arr[1] != "Article summary forbidden":
            try:
                article_nlp = Article(parsed_arr[0])
                article_nlp.download()
                article_nlp.parse()
                article_nlp.nlp()

                if (4 * len(article_nlp.summary)) < len(summary):
                    summary = article_nlp.summary
            except:
                pass

        parsed_articles[source_id] = [parsed_arr[0], parsed_arr[1], summary, bias, parsed_arr[3]]

    sentiments = sentiment_analysis(full_texts)
    return parsed_articles, sentiments

def analyze_article(url):
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    parsed_article = Article(url, config = config)
    parsed_article.download()
    parsed_article.parse()

    title = parsed_article.title
    image = parsed_article.top_image

    parsed_article.nlp()

    sentiment_dict = sentiment_analysis({'article_analysis' : parsed_article.summary})

    sentiment_list = sentiment_dict['article_analysis']

    return title, image, parsed_article.keywords, parsed_article.summary, sentiment_list
