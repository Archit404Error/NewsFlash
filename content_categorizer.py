import os

import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

"""
Topic List(Provided by API)
Arts, Business, Computers, Games, Health, Home, Recreation, Science, Society and Sports
"""


def classify_topic(titles) -> str:
    # Set up necessary headers for API
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token " + os.environ.get("categorization_api_key"),
    }

    # Set up query parameters for UClassify API
    query_params = {"texts": titles}

    # Format endpoint based on classifier publisher and classifier needed
    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format(
        "uclassify", "topics"
    )

    # Send get request to API and store response
    res = requests.post(endpoint_url, headers=headers, json=query_params)
    res_json = res.json()

    classifications = []

    for i, res_dict in enumerate(res_json):
        if "classification" in res_dict:
            category_list = res_dict["classification"]
            ordered_cats = sorted(category_list, key=lambda cat_dict: 1 - cat_dict["p"])
            classifications.append(ordered_cats[0]["className"])
        else:
            classifications.append("")

    return classifications


def sentiment_analysis(texts):
    # Set up necessary headers for API
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token " + os.environ.get("categorization_api_key"),
    }

    # Set up query parameters for UClassify API
    query_params = {"texts": texts}

    # Format endpoint based on classifier publisher and classifier needed
    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format(
        "uclassify", "sentiment"
    )

    # Send get request to API and store response
    res = requests.post(endpoint_url, headers=headers, json=query_params)
    res_json = res.json()

    classifications = []

    # 0th index of each res is negative val, and 1st ind is pos val
    for i, text_res in enumerate(res_json):
        text_res = text_res["classification"]
        if text_res[0]["p"] < text_res[1]["p"]:
            classifications[i] = ["positive", text_res[1]["p"]]
        else:
            classifications[i] = ["negative", text_res[0]["p"]]

    return classifications
