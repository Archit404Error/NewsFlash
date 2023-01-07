import time


class CachedData:
    def __init__(self, cached_arr):
        self.topic = cached_arr[0]
        self.parsed_articles = cached_arr[1]
        self.sentiments = cached_arr[2]
        self.times_queried = cached_arr[3]
        self.time_at_query = cached_arr[4]

    def contains_topic(self, topic):
        found_in_desc = False
        for _, parsed_arr in self.parsed_articles.items():
            if (parsed_arr[1] and topic in parsed_arr[1]) or (
                parsed_arr[2] and topic in parsed_arr[2]
            ):
                found_in_desc = True
        return self.topic == topic or found_in_desc

    def is_fresh(self):
        return (time.time() - self.time_at_query) / (24 * 60 * 60) < 1

    def to_list(self):
        return [
            self.topic,
            self.parsed_articles,
            self.sentiments,
            self.times_queried,
            self.time_at_query,
        ]
