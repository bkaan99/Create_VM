import requests
import json
def get_vm_config(headersWithCookie,vmIdList,nodeName):
    vmIdListToReturn = []
    vmConfigResultList = []
    for i, item in enumerate(vmIdList):
        urlToSendRequest = "https://10.14.46.11:8006/api2/extjs/nodes/"+nodeName+"/qemu/"+str(item)+"/config"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        vmConfigResultList.append(vmConfigResult["data"])
        vmIdListToReturn.append(item)
    return vmConfigResultList , vmIdListToReturn




