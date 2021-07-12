import requests
from newspaper import *
import json
from summary import summarize_text
import os
import datetime, time
import dateutil.parser
from dotenv import load_dotenv
from content_categorizer import classify_topic, sentiment_analysis

#Load environment
load_dotenv()

def get_news(sources, topic) -> tuple[str, str]:

    source_str = ""

    for source, found_val in sources.items():
        source_str += source + ", "

    source_str = source_str[0 : len(source_str) - 2]
    print(source_str)

    #Get date for one week ago to set earliest possible news date
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days = 7)
    week_ago = week_ago.isoformat()

    #Set up parameters for api query
    query_params = {
      "sources" : source_str,
      "qInTitle" : "+{}".format(topic),
      "language" : "en",
      "from" : week_ago,
      "apiKey" : os.environ.get("scraper-api-key")
    }

    endpoint_url = "https://newsapi.org/v2/everything"

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    #If the resonse contains error code, break and return error
    if "code" in res_json.keys():
        return {'No Source Found' : ['http://news-flash-proj.herokuapp.com', 'No article found', res_json["code"]]}

    #Store response articles
    articles = res_json["articles"]

    #Sort articles by date published
    articles.sort(key = lambda item: dateutil.parser.parse(item["publishedAt"]).timestamp() * -1)

    if len(articles) == 0:
        return {'No Source Found' : ['http://news-flash-proj.herokuapp.com', 'No article found', 'No recent news on the topic of ' + topic]}

    parsed_articles = {}

    for article in articles:
        source_id = article["source"]["id"]
        if not source_id in sources.keys():
            sources[source_id] = False
        article_from_id_exists = sources[source_id]
        if article_from_id_exists == False:
            article_url = article["url"]
            newspaper_article = Article(article_url)
            newspaper_article.download()
            try:
                newspaper_article.parse()
                parsed_articles[source_id] = [article_url, newspaper_article.title, newspaper_article.text]
            except:
                parsed_articles[source_id] = [article_url, "Article summary forbidden", "The source prevented automatic article summarization, but the full article can still be read via the link."]
            sources[article["source"]["id"]] = True

    return parsed_articles

def get_top(country):
    #Get date for one week ago to set earliest possible news date
    today = datetime.date.today()

    #Format parameters for API query
    query_params = {
      "country" : "{}".format(country),
      "language" : "en",
      "from" : today,
      "apiKey" : os.environ.get("scraper-api-key")
    }

    endpoint_url = "https://newsapi.org/v2/top-headlines"

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    articles = res_json["articles"]

    article_infos = [{}, time.time()]
    full_texts = {}

    for article in articles:
        title = article["title"]
        source = article["source"]["name"]

        title = title.replace(" " + source, "")
        title = title[0 : len(title) - 2]
        dash_last_occur = title.rfind('-')
        if dash_last_occur > 0:
            title = title[:dash_last_occur]

        full_texts[source] = title

        article_infos[0][source] = [title, article["content"], article["url"]]

    class_res = classify_topic(full_texts)
    sen_res = sentiment_analysis(full_texts)

    for article in articles:
        source = article["source"]["name"]
        article_infos[0][source].append(class_res[source])
        article_infos[0][source].append(sen_res[source])

    return article_infos
