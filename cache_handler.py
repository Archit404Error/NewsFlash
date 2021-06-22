from newsflash import collect_news
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
            #Account for keywords by searching for topic in description
            if stored[0] == topic or topic in stored[2].values():
                if (time.time() - stored[6]) / (24 * 60 * 60) < 1:
                    #Get cached values to decrease query time
                    sources = stored[1]
                    outlet_summaries = stored[2]
                    biases = stored[3]
                    article_links = stored[4]
                    #Increment times queried value
                    times_queried = stored[5] + 1
                    time_at_query = stored[6]
                else:
                    sources, outlet_summaries, biases, article_links = collect_news(topic)
                    times_queried = 1
                    time_at_query = time.time()
                #Reset the value of this object and add it to json file
                cache.seek(0)
                cached_list[cached_list.index(stored)] = [topic, sources, outlet_summaries, biases, article_links, times_queried, time_at_query]
                json.dump(cached_list, cache)
                cache.truncate()
    else:
        #Get values from collect_news function
        sources, outlet_summaries, biases, article_links = collect_news(topic)
        times_queried = 1
        time_at_query = time.time()
        #Create json data, append it to cached_list, and dump into file
        json_data = [topic, sources, outlet_summaries, biases, article_links, times_queried, time_at_query]
        cache.seek(0)
        cached_list.append(json_data)
        json.dump(cached_list, cache)
        cache.truncate()

    #Send back collected values necessary to displaying articles
    return sources, outlet_summaries, biases, article_links

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
