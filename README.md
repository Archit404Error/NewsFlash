# Newsflash

## What it does

Newsflash is a program built to enable people to quickly read up on current news,
all while getting multiple viewpoints from across the aisle. Newsflash pulls
the most recent news from a given topic, summarizes the articles, and displays articles
from several sources with different viewpoints to the user. In other words,
users no longer have to seek out different opinions manually in order to eliminate bias
from the news they are getting.

## Usage

The following command will start the flask server

```bash
usage: python3 main.py
```

Upon starting the server, the program will begin running at `127.0.0.1:5000/`

Additionally, it is necessary to create a `.env` file in order to store API keys that will be loaded into different parts of your program.

Your API keys should be formatted as such: `categorization-api-key: [insert here]` and `scraper-api-key: [insert here]`

## Program Structure

All scraping and data collection happens at the `/api` page, where all user requests are sent and all responses are received from. The reasoning behind this is to provide for easier implementation and communication between mobile and web clients.

In other words, both the mobile app as well as the website utilize `/api` on the server in order to display information to the user. Hence, any changes to the core logic(back-end) of the program should be done on `/api`.

This project also makes use of a cache to decrease response times for the end user, refreshing the cache only after the program notices the data has gone stale (~1 day old) upon the user making a request. Since there is not a particularly large amount of data that needs to be stored, I chose to store the data in a json file, mainly for the sake of faster query times.

## APIs Used

The APIs used in the creation of this project were [NewsAPI](https://newsapi.org), in order to gather and scrape articles, as well as [UClassify](https://www.uclassify.com), to perform content categorization and sentiment analysis.

## Other Important Info

It is also important to recognize that summaries in this project were generated via a manual implementation of natural language processing, which may be outsourced to another API in the future.
