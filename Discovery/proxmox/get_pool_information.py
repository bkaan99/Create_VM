import requests
import json
import pandas as pd
def get_pool_information(headersWithCookie, poolName):
    vmConfigResultList = []
    urlToSendRequest = "https://10.14.46.11:8006/api2/extjs/pools/"+poolName
    vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
    vmConfigResult = json.loads(vmConfigResult)
    return vmConfigResult["data"]
