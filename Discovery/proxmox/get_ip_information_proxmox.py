import requests
import json

def get_ip_given_vm(environmentIp, nodeName, vmIdList, headersWithCookie):
    vmIdListToReturn = []
    keyList = []
    valueList = []
    for i in range(len(vmIdList)):
        urlToSendRequest = "https://"+environmentIp+"/api2/extjs/nodes/"+nodeName+"/qemu/"+str(vmIdList[i])+"/agent/network-get-interfaces"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        if vmConfigResult["data"] == None:
            keyList.append("error")
            valueList.append(vmConfigResult["message"])
            vmIdListToReturn.append(vmIdList[i])
        else:
            valueList.append(vmConfigResult["data"]["result"])
            keyList.append("ip_config")
            vmIdListToReturn.append(vmIdList[i])

    return keyList, valueList, vmIdListToReturn

