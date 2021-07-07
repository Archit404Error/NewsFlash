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
            for source_id, parsed_arr in stored[1].items():
                if (parsed_arr[1] != None and topic in parsed_arr[1]) or (parsed_arr[2] != None and topic in parsed_arr[2]):
                    found_in_desc = True
            #Account for keywords by searching for topic in description
            if stored[0] == topic or found_in_desc:
                if (time.time() - stored[4]) / (24 * 60 * 60) < 1:
                    #Get cached values to decrease query time
                    parsed_articles = stored[1]
                    sentiments = stored[2]
                    #Increment times queried value
                    times_queried = stored[3] + 1
                    time_at_query = stored[4]
                else:
                    parsed_articles, sentiments = collect_news(topic)
                    times_queried = 1
                    time_at_query = time.time()
                #Reset the value of this object and add it to json file
                cache.seek(0)
                #Use our newly created vars to edit cache vals for this topic
                cached_list[cached_list.index(stored)] = [stored[0], parsed_articles, sentiments, times_queried, time_at_query]
                json.dump(cached_list, cache)
                cache.truncate()
    else:
        #Get values from collect_news function
        parsed_articles, sentiments = collect_news(topic)
        times_queried = 1
        time_at_query = time.time()
        #Create json data, append it to cached_list, and dump into file
        json_data = [topic, parsed_articles, sentiments, times_queried, time_at_query]
        cache.seek(0)
        cached_list.append(json_data)
        json.dump(cached_list, cache)
        cache.truncate()

    #Send back collected values necessary to displaying articles
    return parsed_articles, sentiments

def trending_news(cache_path):
    cache = open(cache_path, 'r+')

    try:
        cached_list = json.load(cache)
    except:
        cached_list = []

    cached_list.sort(key=lambda stored: -1 * stored[3])
    cached_list = filter(lambda story: story[3] > 1, cached_list)

    trending_topics = []

    for article_obj in cached_list:
        trending_topics.append(article_obj[0])

    return trending_topics

def top_news(cache_path):
    cache = open(cache_path, 'r+')

    try:
        top_articles = json.load(cache)
    except:
        top_articles = [{}, time.time()]

    #Reopen cache file so we can re-read from it
    cache = open(cache_path, 'r+')

    if len(top_articles[0]) == 0 or ((time.time() - top_articles[1]) / (60 * 60 * 24)) >= 1:
        top_articles = get_top("us")
        cache.seek(0)
        json.dump(top_articles, cache)
        cache.truncate()

    return top_articles
