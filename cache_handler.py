from newsflash import collect_news
from news_scraper import get_top
import json, time

def cache_query(cache_path, topic):
    cache = open(cache_path, 'r+')
    try:
        cached_list = json.load(cache)
    except:
        #Occurs if we fail to load cache json(only occurs when cache is empty)
        cached_list = []
    #Reopen cache file so we can re-read from it
    cache = open(cache_path, 'r+')
    if topic in cache.read():
        for stored in cached_list:
            found_in_desc = False
            for key, val in stored[2].items():
                if (val[0] != None and topic in val[0]) or (val[1] != None and topic in val[1]):
                    found_in_desc = True
            #Account for keywords by searching for topic in description
            if stored[0] == topic or found_in_desc:
                if (time.time() - stored[6]) / (24 * 60 * 60) < 1:
                    #Get cached values to decrease query time
                    sources = stored[1]
                    outlet_summaries = stored[2]
                    biases = stored[3]
                    article_links = stored[4]
                    #Increment times queried value
                    times_queried = stored[5] + 1
                    time_at_query = stored[6]
                    sentiments = stored[7]
                else:
                    sources, outlet_summaries, biases, article_links, sentiments = collect_news(topic)
                    times_queried = 1
                    time_at_query = time.time()
                #Reset the value of this object and add it to json file
                cache.seek(0)
                cached_list[cached_list.index(stored)] = [stored[0], sources, outlet_summaries, biases, article_links, times_queried, time_at_query, sentiments]
                json.dump(cached_list, cache)
                cache.truncate()
    else:
        #Get values from collect_news function
        sources, outlet_summaries, biases, article_links, sentiments = collect_news(topic)
        times_queried = 1
        time_at_query = time.time()
        #Create json data, append it to cached_list, and dump into file
        json_data = [topic, sources, outlet_summaries, biases, article_links, times_queried, time_at_query, sentiments]
        cache.seek(0)
        cached_list.append(json_data)
        json.dump(cached_list, cache)
        cache.truncate()

    #Send back collected values necessary to displaying articles
    return sources, outlet_summaries, biases, article_links, sentiments

def trending_news(cache_path):
    cache = open(cache_path, 'r+')

    try:
        cached_list = json.load(cache)
    except:
        cached_list = []

    cached_list.sort(key=lambda stored: -1 * stored[5])
    cached_list = filter(lambda story: story[5] > 1, cached_list)

    trending_topics = []

    for article_obj in cached_list:
        trending_topics.append(article_obj[0])

    return trending_topics

def top_news(cache_path):
    cache = open(cache_path, 'r+')

    try:
        top_articles = json.load(cache)
    except:
        top_articles = {}

    #Reopen cache file so we can re-read from it
    cache = open(cache_path, 'r+')

    if len(top_articles) == 0:
        top_articles = get_top("us")
        cache.seek(0)
        json.dump(top_articles, cache)
        cache.truncate()

    return top_articles
