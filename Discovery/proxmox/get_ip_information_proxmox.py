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
            pass
        else:
            valueList.append(vmConfigResult["data"]["result"])
            keyList.append("ip_config")
            vmIdListToReturn.append(vmIdList[i])
    return keyList, valueList, vmIdListToReturn

        # try:
        #     for c in range(len(vmConfigResult["data"]["result"])):
        #         keyList = vmConfigResult["data"]["result"][c].keys()
        #         for key in keyList:
        #             valueList.append(vmConfigResult["data"]["result"][c][key])
        #     vmIdListToReturn.append(vmIdList[i])
        # except:
        #     pass
