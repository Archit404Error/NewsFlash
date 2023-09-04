import json
import os
import time

from cache_models import CachedData
from news_scraper import get_top
from newsflash import collect_news


def cache_query(cache_path, topic):
    cache = open(cache_path, "w+")
    try:
        cached_list = json.load(cache)
    except:
        # Occurs if we fail to load cache json(only occurs when cache is empty)
        cached_list = []
    # Reopen cache file so we can re-read from it
    cache = open(cache_path, "w+")
    parsed_articles = {}
    if topic in cache.read():
        for stored in cached_list:
            stored_article = CachedData(stored)
            # Account for keywords by searching for topic in description
            if stored_article.contains_topic(topic):
                if stored_article.is_fresh():
                    # Get cached values to decrease query time
                    parsed_articles = stored_article.parsed_articles
                    sentiments = stored_article.sentiments
                    # Increment times queried value
                    times_queried = stored_article.times_queried + 1
                    time_at_query = stored_article.time_at_query
                else:
                    parsed_articles, sentiments = collect_news(topic)
                    times_queried = 1
                    time_at_query = time.time()
                # Reset the value of this object and add it to json file
                cache.seek(0)
                # Use our newly created vars to edit cache vals for this topic
                cached_list[cached_list.index(stored)] = [
                    stored_article.topic,
                    parsed_articles,
                    sentiments,
                    times_queried,
                    time_at_query,
                ]
                json.dump(cached_list, cache)
                cache.truncate()
    else:
        # Get values from collect_news function
        parsed_articles, sentiments = collect_news(topic)
        times_queried = 1
        time_at_query = time.time()
        # Create json data, append it to cached_list, and dump into file
        json_data = [topic, parsed_articles, sentiments, times_queried, time_at_query]
        cache.seek(0)
        cached_list.append(json_data)
        json.dump(cached_list, cache)
        cache.truncate()

    # Send back collected values necessary to displaying articles
    return parsed_articles, sentiments


def trending_news(cache_path):
    path = Path(cache_path)
    path.touch(exist_ok=True)

    cache = open(cache_path, "w+")

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
    if not os.path.exists(cache_path):
        open(cache_path, "w+").close()
        top_articles = [[], time.time()]
    else:
        cache = open(cache_path, "r")
        top_articles = json.load(cache)

    if (
        len(top_articles[0]) == 0
        or ((time.time() - top_articles[1]) / (60 * 60 * 24)) >= 1
    ):
        # Open and clear cache
        cache = open(cache_path, "w+")
        top_articles = get_top("us")
        cache.seek(0)
        json.dump(top_articles, cache)
        cache.truncate()
    else:
        print("using cached")

    return top_articles


def clear_caches(cache_paths):
    for cache in cache_paths:
        curr_cache = open(cache, "w+")
        curr_cache.seek(0)
        curr_cache.truncate()
