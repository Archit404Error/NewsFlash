import requests
import os
from dotenv import load_dotenv

#Load environment
load_dotenv()

'''
Topic List(Provided by API)
Arts, Business, Computers, Games, Health, Home, Recreation,Science, Society and Sports
'''

def classify_topic(topic) -> str:
    #Set up query parameters for UClassify API
    query_params = {
        "readKey" : os.environ.get("categorization-api-key"),
        "text" : topic
    }

    #Format endpoint based on classifier publisher and classifier needed
    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format("uclassify", "topics")

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    # Sort res by key, figuring out which topic was most likely match
    ordered_res = dict(sorted(res_json.items(), key=lambda item: 1 - item[1]))
    # Gets the first key in the ordered dict(most confident)
    predicted_topic = (next(iter(ordered_res)))
    return predicted_topic

def sentiment_analysis(text) -> str:
    #Set up query parameters for UClassify API
    query_params = {
        "readKey" : os.environ.get("categorization-api-key"),
        "text" : text
    }

    #Format endpoint based on classifier publisher and classifier needed
    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format("uclassify", "sentiment")

    #Send get request to API and store response
    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    if res_json['positive'] > res_json['negative']:
        return ['positive', res_json['positive']]
    return ['negative', res_json['negative']]
