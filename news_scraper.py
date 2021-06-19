import requests
from newspaper import *
import json
from summary import summarize_text
import os
from dotenv import load_dotenv

#Load environment
load_dotenv()

def get_news(source, topic) -> tuple[str, str]:
    #Set up parameters for api query
    query_params = {
      "sources" : source,
      "q" : "{}".format(topic),
      "apiKey" : os.environ.get("scraper-api-key")
    }

    endpoint_url = "https://newsapi.org/v2/everything"

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    #If the resonse contains error code, break and return error
    if "code" in res_json.keys():
        print("ERROR: " + res_json["code"] + " " + source)
        return res_json["code"]

    #Store response articles
    articles = res_json["articles"]

    if len(articles) == 0:
        return None, "No articles found on the subject of " + topic + " from the source " + source

    #Get URL of first returned article to find most recent/relevant article from source
    article_url = articles[0]["url"]

    #Parse article from URL and store text
    newspaper_article = Article(article_url)
    newspaper_article.download()
    newspaper_article.parse()
    return article_url, newspaper_article.text

def get_trending() -> dict[str, list[str, str]]:
    #Set up API query parameters
    query_params = {
      "country" : "us",
      "apiKey" : os.environ.get("scraper-api-key")
    }

    endpoint_url = "https://newsapi.org/v2/top-headlines"

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()
    articles = res_json["articles"]

    #Create outlet summaries dict to store source, article url, and text
    outlet_summaries = {}

    for article in articles:
        #Get article URL and parse it using newspaper3k
        article_url = article["url"]
        newspaper_article = Article(article_url)
        try:
            newspaper_article.download()
            newspaper_article.parse()
        except:
            continue
        #Store the article publisher into source_name variable(which will be used as dict key)
        source_name = (article["source"])["name"]
        outlet_summaries[source_name] = [article_url, summarize_text(newspaper_article.text)]

    return outlet_summaries
