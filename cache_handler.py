from newsflash import collect_news
import json

def cache_query(cache_path, topic):
    cache = open(cache_path, 'r+')
    try:
        cached_list = json.load(cache)
    except:
        cached_list = []
    cache = open(cache_path, 'r+')
    if topic in cache.read():
        for stored in cached_list:
            if stored[0] == topic or topic in stored[2].values():
                sources = stored[1]
                outlet_summaries = stored[2]
                biases = stored[3]
                article_links = stored[4]
                times_queried = stored[5] + 1
                cache.seek(0)
                cached_list[cached_list.index(stored)] = [topic, sources, outlet_summaries, biases, article_links, times_queried]
                json.dump(cached_list, cache)
                cache.truncate()
    else:
        sources, outlet_summaries, biases, article_links = collect_news(topic)
        times_queried = 1
        json_data = [topic, sources, outlet_summaries, biases, article_links, times_queried]
        cache.seek(0)
        cached_list.append(json_data)
        json.dump(cached_list, cache)
        cache.truncate()

    return sources, outlet_summaries, biases, article_links
