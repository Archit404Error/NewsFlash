import datetime
import json
import os
import time

import dateutil.parser
import requests
from dotenv import load_dotenv
from newspaper import *

from content_categorizer import classify_topic, sentiment_analysis
from summary import summarize_text

#Load environment
load_dotenv()

def get_news(sources, topic):

    source_str = ""

    for source, found_val in sources.items():
        source_str += source + ", "

    source_str = source_str[0 : len(source_str) - 2]

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
      "apiKey" : os.environ.get("scraper_api_key")
    }

    endpoint_url = "https://newsapi.org/v2/everything"

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    #If the resonse contains error code, break and return error
    if "code" in res_json.keys():
        return {'No Source Found' : ['http://127.0.0.1:5000', 'No article found', res_json["code"], "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/1200px-Question_mark_%28black%29.svg.png"]}

    #Store response articles
    articles = res_json["articles"]

    #Sort articles by date published
    articles.sort(key = lambda item: dateutil.parser.parse(item["publishedAt"]).timestamp() * -1)

    if len(articles) == 0:
        #Create looser params
        query_params = {
          "sources" : source_str,
          "q" : "{}".format(topic),
          "language" : "en",
          "from" : week_ago,
          "apiKey" : os.environ.get("scraper_api_key")
        }
        res = requests.get(endpoint_url, params=query_params)
        res_json = res.json()

        #Store response articles
        articles = res_json["articles"]

        if len(articles) == 0:
            #Return if still nothing found
            return {'No Source Found' : ['http://127.0.0.1:5000', 'No article found', 'No recent news on the topic of ' + topic, "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/1200px-Question_mark_%28black%29.svg.png"]}

    parsed_articles = {}

    for article in articles:
        source_id = article["source"]["id"]
        if not source_id in sources.keys():
            sources[source_id] = False
        article_from_id_exists = sources[source_id]
        if article_from_id_exists == False:
            article_url = article["url"]

            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
            config = Config()
            config.browser_user_agent = user_agent

            newspaper_article = Article(article_url, config = config)
            newspaper_article.download()
            try:
                newspaper_article.parse()
                parsed_articles[source_id] = [article_url, newspaper_article.title, newspaper_article.text, newspaper_article.top_image]
            except Exception as e:
                print(e)
                parsed_articles[source_id] = [article_url, "Article summary forbidden", "The source prevented automatic article summarization, but the full article can still be read via the link.", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/1200px-Question_mark_%28black%29.svg.png"]
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
      "apiKey" : os.environ.get("scraper_api_key")
    }

    endpoint_url = "https://newsapi.org/v2/top-headlines"

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    print(res_json)
    articles = res_json["articles"]

    article_infos = [{}, time.time()]
    full_texts = {}

    for article in articles:
        title = article["title"]
        source = article["source"]["name"]
        image = ""

        try:
            config = Config()
            config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

            newspaper_article = Article(article["url"], config = config)
            newspaper_article.download()
            newspaper_article.parse()
            title = newspaper_article.title
            image = newspaper_article.top_image
            newspaper_article.nlp()
            keywords = newspaper_article.keywords
        except:
            title = title.replace(" " + source, "")
            title = title[0 : len(title) - 2]
            dash_last_occur = title.rfind('-')
            if dash_last_occur > 0 and title[dash_last_occur + 1:].strip() == source:
                title = title[:dash_last_occur]
            image = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/1200px-Question_mark_%28black%29.svg.png"
            keywords = []

        full_texts[source] = title

        article_infos[0][source] = [title, article["content"], article["url"], image, keywords]

    class_res = classify_topic(full_texts)
    sen_res = sentiment_analysis(full_texts)

    for article in articles:
        source = article["source"]["name"]
        article_infos[0][source].append(class_res[source])
        article_infos[0][source].append(sen_res[source])

    return article_infos
