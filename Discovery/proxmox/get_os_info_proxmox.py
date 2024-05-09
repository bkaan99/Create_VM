import requests
import json

def get_os_information(environmentIp, nodeName, vmIdList, headersWithCookie):
    vmIdListToReturn = []
    keyList = []
    valueList = []
    for i in range(len(vmIdList)):
        urlToSendRequest = "https://"+environmentIp+"/api2/extjs/nodes/"+nodeName+"/qemu/"+str(vmIdList[i])+"/agent/get-osinfo"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        if vmConfigResult["data"] == None:
            keyList.append("error")
            valueList.append(vmConfigResult["message"])
            vmIdListToReturn.append(vmIdList[i])
        else:
            valueList.append(vmConfigResult["data"]["result"])
            keyList.append("osinfo_config")
            vmIdListToReturn.append(vmIdList[i])
    return keyList, valueList, vmIdListToReturn