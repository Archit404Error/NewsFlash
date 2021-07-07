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
    print(res_json.items())
    ordered_res = dict(sorted(res_json.items(), key=lambda item: 1 - float(item[1])))
    # Gets the first key in the ordered dict(most confident)
    predicted_topic = (next(iter(ordered_res)))
    return predicted_topic

def sentiment_analysis(texts) -> dict[str, float]:
    #Set up necessary headers for API
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "Token " + os.environ.get("categorization-api-key")
    }

    #Set up query parameters for UClassify API
    query_params = {
        "texts" : list(texts.values())
    }

    #Format endpoint based on classifier publisher and classifier needed
    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format("uclassify", "sentiment")

    #Send get request to API and store response
    res = requests.post(endpoint_url, headers=headers, json=query_params)
    res_json = res.json()

    classifications = {}

    #0th index of each res is negative val, and 1st ind is pos val
    for i, text_res in enumerate(res_json):
        text_res = text_res["classification"]
        sources = list(texts.keys())
        if text_res[0]['p'] < text_res[1]['p']:
            classifications[sources[i]] = ['positive', text_res[1]['p']]
        else:
            classifications[sources[i]] = ['negative', text_res[0]['p']]

    return classifications
