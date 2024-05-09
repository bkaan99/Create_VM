import requests
import json

def get_host_name(environmentIp, nodeName, vmIdList, headersWithCookie):
    vmIdListToReturn = []
    keyList = []
    valueList = []
    for i in range(len(vmIdList)):
        urlToSendRequest = "https://"+environmentIp+"/api2/extjs/nodes/"+nodeName+"/qemu/"+str(vmIdList[i])+"/agent/get-host-name"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        if vmConfigResult["data"] == None:
            pass
        else:
            valueList.append(vmConfigResult["data"]["result"])
            keyList.append("hostname_config")
            vmIdListToReturn.append(vmIdList[i])
    return keyList, valueList, vmIdListToReturn