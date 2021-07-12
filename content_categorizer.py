import requests
import os
from dotenv import load_dotenv

#Load environment
load_dotenv()

'''
Topic List(Provided by API)
Arts, Business, Computers, Games, Health, Home, Recreation, Science, Society and Sports
'''

def classify_topic(titles) -> str:
    #Set up necessary headers for API
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "Token " + os.environ.get("categorization-api-key")
    }

    #Set up query parameters for UClassify API
    query_params = {
        "texts" : list(titles.values())
    }

    #Format endpoint based on classifier publisher and classifier needed
    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format("uclassify", "topics")

    #Send get request to API and store response
    res = requests.post(endpoint_url, headers=headers, json=query_params)
    res_json = res.json()

    classifications = {}
    sources = list(titles.keys())

    for i, res_dict in enumerate(res_json):
        print(res_dict)
        category_list = res_dict["classification"]
        ordered_cats = sorted(category_list, key = lambda cat_dict : 1 - cat_dict['p'])
        classifications[sources[i]] = ordered_cats[0]['className']

    return classifications

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
