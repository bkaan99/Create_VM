import requests
import json

def get_ip_given_vm(environmentIp, nodeName, vmIdList, headersWithCookie):
    vmIdListToReturn = []
    keyList = []
    valueList = []
    for i, item in enumerate(vmIdList):
        urlToSendRequest = "https://"+environmentIp+"/api2/extjs/nodes/"+nodeName+"/qemu/"+str(item)+"/agent/network-get-interfaces"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        if vmConfigResult["data"] is None:
            keyList.append("error")
            valueList.append(vmConfigResult["message"])
            vmIdListToReturn.append(item)
        else:
            valueList.append(vmConfigResult["data"]["result"])
            keyList.append("ip_config")
            vmIdListToReturn.append(item)

    return keyList, valueList, vmIdListToReturn

