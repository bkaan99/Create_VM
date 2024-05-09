import requests
import json

def get_pool_names(headersWithCookie):
    poolNames = []
    vmConfigResultList = []
    urlToSendRequest = "https://10.14.46.11:8006/api2/extjs/pools/"
    vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
    vmConfigResult = json.loads(vmConfigResult)
    for config in vmConfigResult["data"]:
        poolNames.append(config.get("poolid"))
    return poolNames
