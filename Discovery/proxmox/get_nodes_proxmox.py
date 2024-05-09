import requests
import json

def get_nodes(headers,url):
    resultFromRequest = requests.get(url,headers=headers,verify=False).text
    resultFromRequest = json.loads(resultFromRequest)
    return resultFromRequest["data"]