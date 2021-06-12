import requests

'''
Topic List(Provided by API)
Arts, Business, Computers, Games, Health, Home, Recreation,Science, Society and Sports
'''

def classify_topic(topic):
    query_params = {
        "readKey" : "d2HXLjz3dWcM",
        "text" : topic
    }

    endpoint_url = "https://api.uclassify.com/v1/{}/{}/classify".format("uclassify", "topics")

    res = requests.get(endpoint_url, params=query_params)
    res_json = res.json()

    # Sort res by key, figuring out which topic was most likely match
    ordered_res = dict(sorted(res_json.items(), key=lambda item: 1 - item[1]))
    # Gets the first key in the ordered dict(most confident)
    predicted_topic = (next(iter(ordered_res)))
    return predicted_topic

classify_topic("French Presidential Election")
