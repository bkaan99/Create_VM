import requests
import json

def get_disk_information(environmentIp, nodeName, vmIdList, headersWithCookie):
    vmIdListToReturn = []
    keyList = []
    valueList = []
    for i, item in enumerate(vmIdList):
        urlToSendRequest = "https://"+environmentIp+"/api2/extjs/nodes/"+nodeName+"/qemu/"+str(item)+"/agent/get-fsinfo"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        if vmConfigResult["data"] is None:
            keyList.append("error")
            valueList.append(vmConfigResult["message"])
            vmIdListToReturn.append(item)
        else:
            valueList.append(vmConfigResult["data"]["result"])
            keyList.append("disk_config")
            vmIdListToReturn.append(item)
    return keyList, valueList, vmIdListToReturn