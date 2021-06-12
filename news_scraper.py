import requests
from newspaper import *
import json
from summary import summarize_text
import os
from dotenv import load_dotenv

#Load environment
load_dotenv()

def get_news(source, topic):
    query_params = {
      "sources" : source,
      "q" : "{}".format(topic),
      "apiKey" : os.environ.get("scraper-api-key")
    }

    endpoint_url = "https://newsapi.org/v2/everything"

    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()
    if "code" in res_json.keys():
        print("ERROR: " + res_json["code"] + " " + source)
        return res_json["code"]
    articles = res_json["articles"]

    if len(articles) == 0:
        return None, "No articles found on the subject of " + topic + " from the source " + source

    article_url = articles[0]["url"]

    newspaper_article = Article(article_url)
    newspaper_article.download()
    newspaper_article.parse()
    return article_url, newspaper_article.text

def get_trending():
    query_params = {
      "country" : "us",
      "apiKey" : "275590f4b1cb48608969171d4acd641b"
    }

    endpoint_url = "https://newsapi.org/v2/top-headlines"

    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()
    articles = res_json["articles"]

    outlet_summaries = {}

    for article in articles:
        article_url = article["url"]
        newspaper_article = Article(article_url)
        try:
            newspaper_article.download()
            newspaper_article.parse()
        except:
            continue
        source_name = (article["source"])["name"]
        print(newspaper_article.title)
        outlet_summaries[source_name] = [article_url, summarize_text(newspaper_article.text)]

    return outlet_summaries
