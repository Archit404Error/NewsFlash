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

def get_news(source, topic) -> tuple[str, str]:

    #Get date for one week ago to set earliest possible news date
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days = 7)
    week_ago = week_ago.isoformat()

    #Set up parameters for api query
    query_params = {
      "sources" : source,
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
        return None, "Error", res_json["code"]

    #Store response articles
    articles = res_json["articles"]

    #Sort articles by date published
    articles.sort(key = lambda item: dateutil.parser.parse(item["publishedAt"]).timestamp() * -1)

    if len(articles) == 0:
        return None, "No article found", "No articles found on the subject of " + topic + " from the source " + source

    #Get URL of first returned article to find most recent/relevant article from source
    article_url = articles[0]["url"]

    #Parse article from URL and store text
    newspaper_article = Article(article_url)
    try:
        newspaper_article.download()
        newspaper_article.parse()
        return article_url, newspaper_article.title, newspaper_article.text
    except:
        return "http://news-flash-proj.herokuapp.com", "No Article Found", "No Article Found"

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

    for article in articles:
        title = article["title"]
        source = article["source"]["name"]

        title = title.replace(" " + source, "")
        title = title[0 : len(title) - 2]
        dash_last_occur = title.rfind('-')
        if dash_last_occur > 0:
            title = title[:dash_last_occur]

        article_infos[0][source] = [title, article["content"], article["url"], classify_topic(title), sentiment_analysis(title)]

    return article_infos
