import json
import requests
import base64
import psycopg2
import pandas as pd
import sys
from sqlalchemy import create_engine
from datetime import datetime
from Discovery.proxmox import get_vm_id_list_proxmox, get_ip_information_proxmox, get_disk_volumes_proxmox, \
    get_os_info_proxmox


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def append_vm_info(vmID, key, value, additional_info=''):
    try:
        append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, virtualizationEnvironmentIp, virtualizationEnvironmentIp,
                                      notes=f"{additional_info}")
    except:
        pass


def get_nodes(headers,url):
    resultFromRequest = requests.get(url,headers=headers,verify=False).text
    resultFromRequest = json.loads(resultFromRequest)
    return resultFromRequest["data"]

def get_node_information_from_json(jsonWithNodes):
    listOfNodeNames = []
    for i in range(len(jsonWithNodes)):
        listOfNodeNames.append(jsonWithNodes[i]["node"])
    return listOfNodeNames

def discover_proxmox_environment(nodeName):
    url = "https://10.14.46.11:8006/api2/extjs/nodes/"+nodeName+"/qemu"
    discoveredNodeData = get_vm_id_list_proxmox.get_vm_id_list(headersWithCookie, url)
    return discoveredNodeData

def get_id_from_discovered_data(firstDiscoveredJson):
    listOfVMIDS = []
    for i in range(len(firstDiscoveredJson)):
        listOfVMIDS.append(firstDiscoveredJson[i]["vmid"])
    return listOfVMIDS

def get_vm_config(headersWithCookie,vmIdList,nodeName):
    vmIdListToReturn = []
    vmConfigResultList = []
    for i in range(len(vmIdList)):
        urlToSendRequest = "https://10.14.46.11:8006/api2/extjs/nodes/"+nodeName+"/qemu/"+str(vmIdList[i])+"/config"
        vmConfigResult = requests.get(urlToSendRequest, headers=headersWithCookie, verify=False).text
        vmConfigResult = json.loads(vmConfigResult)
        vmConfigResultList.append(vmConfigResult["data"])
        vmIdListToReturn.append(vmIdList[i])
    return vmConfigResultList, vmIdListToReturn

def extract_useful_data_from_vm_config(configList, IdList):
    keys_to_check = [
        "acpi", "affinity", "agent", "arch", "args", "audio0", "autostart",
        "balloon", "bios", "bootdisk", "cdrom", "cicustom", "ciuser",
        "cipassword", "citype", "ciupgrade", "ciuser", "cores", "cpu", "cpulimit",
        "cpuunits", "description", "digest", "efidisk0", "freeze", "hookscript",
        "hostpci", "hotplug", "hugepages", "ivshmem","keephugepages", "keyboard",
        "kvm", "localtime", "lock", "machine","memory", "migrate_downtime",
        "migrate_speed", "name", "nameserver", "numa","onboot", "ostype",
        "parallel", "protection", "reboot","rng0", "scsihw", "searchdomain",
        "serial", "shares","smbios1", "smp", "sockets", "spice_enhancement", "sshkeys",
        "startdate","startup", "tablet", "tags", "tdf", "template", "tpmstate0", "unused",
        "usb", "vcpus", "vga", "vmgenid", "vmstatestorage", "watchdog"
    ]

    for c in range(len(configList)):
        config = configList[c]
        for key in config.keys():
            listOfValuesForDataFrame = []

            if key in keys_to_check:
                keyForInsert = key
                valueForInsert = config[str(key)]
                append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

            elif "boot" == key:
                keyForInsert = key
                valueForInsert = config["boot"]
                try:
                    for t in range(len(valueForInsert.split("=")[1].split(";"))):
                        insertSplittedValue = valueForInsert.split("=")[1].split(";")[t]
                        append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                        append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")


            elif "ide" in key:
                #@TODO Might be edited for different ide results!!
                keyForInsert = key
                valueForInsert = config[key]
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

            elif "ipconfig" in key:
                #@TODO Might be edited for different ipconfig results!!
                keyForInsert = key
                valueForInsert = config[key]
                try:
                    insertSplittedValue = valueForInsert.replace(",","|")
                    append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")



            elif "net" in key:
                #@TODO Will be changed later!!! (got only limited data for net[n])
                keyForInsert = key
                valueForInsert = config[key]
                try:
                    insertSplittedValue = valueForInsert.replace(",","|")
                    append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")


            elif "sata" in key:
                #@TODO Might be edited for different sata results!!
                keyForInsert = key
                valueForInsert = config[key]
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

            elif "scsi" in key:
                #@TODO Might be edited for different scsi results!!
                keyForInsert = key
                valueForInsert = config[key]
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")


            elif "virtio" in key:
                #@TODO Might be edited for different virtio results!!
                keyForInsert = key
                valueForInsert = config[key]
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, insertSplittedValue, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")


if __name__ == "__main__":
    createdDateForAppend = datetime.now()
    versionForAppend = 2
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "Proxmox"
    virtualizationEnvironmentIp = "10.14.46.11:8006"
    dataFrameColumns = ["key", "value", "is_deleted", "version", "created_date", "vm_id",
                        "virtualization_environment_type", "virtualization_environment_ip", "node", "notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)


    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")

    def Convert(string):
        li = list(string.replace(' ', '').split(","))
        return li

    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()
    vmIdList = Convert(mystring)

    login = {
        "username": "root",
        "password": "Aa112233!",
        "realm": "pam",
        "new-format": 1
    }
    headers = {
        "Content-Type": "application/json",
    }
    responseforticket = requests.post("https://10.14.46.11:8006/api2/extjs/access/ticket", headers=headers, json=login,
                                      verify=False)
    headersWithCookie = {
        "Content-Type": "application/json",
        "Cookie": "PVEAuthCookie=" + responseforticket.json().get("data").get("ticket"),
        "Csrfpreventiontoken": responseforticket.json().get("data").get("CSRFPreventionToken"),
    }

    urlToGetNodes = "https://" + str(virtualizationEnvironmentIp) + "/api2/json/nodes/"
    nodesOfGivenEnvironment = get_nodes(headersWithCookie, urlToGetNodes)
    #Node bilgileri
    for node in nodesOfGivenEnvironment:
        node_description = node.items()
        for key, value in node_description:
            append_vm_info(vmID=0, key=key, value=value, additional_info="/api2/json/nodes/")


    clearedNodeInfo = get_node_information_from_json(nodesOfGivenEnvironment)
    for node in clearedNodeInfo:
        discoveredNodeData = discover_proxmox_environment(node)
        #node'a ait vm'lerin bilgileri
        for vm in discoveredNodeData:
            for key, value in vm.items():
                append_vm_info(vmID=vm["vmid"], key=key, value=value, additional_info=f"api2/extjs/nodes/{node}/qemu")

        listOfVMIDS = get_id_from_discovered_data(discoveredNodeData)
        configListOfVms, IdList = get_vm_config(headersWithCookie, listOfVMIDS, node)
        for vm_config, vm_id in zip(configListOfVms, IdList):
            for key, value in vm_config.items():
                append_vm_info(vmID=vm_id, key=key, value=value, additional_info=f"api2/extjs/nodes/{node}/qemu/{vm_id}/config")

        lastDataFrameForInsert = extract_useful_data_from_vm_config(configListOfVms, IdList)

        keyListForIpConfig, ipconfigsOfVms, IdListForIpConfig = get_ip_information_proxmox.get_ip_given_vm(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)

        for t in range(len(keyListForIpConfig)):
            append_dataframe_given_values(keyListForIpConfig[t], str(ipconfigsOfVms[t]), isDeletedValueForAppend,
                                          versionForAppend, createdDateForAppend, IdListForIpConfig[t],
                                          virtualizationEnvironmentType, virtualizationEnvironmentIp, node,
                                          f"api2/extjs/nodes/{node}/qemu/{IdListForIpConfig[t]}/agent/network-get-interfaces")


        keyListForDiskConfig, diskConfigOfVms, IdListForDiskConfig = get_disk_volumes_proxmox.get_disk_information(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)

        for t in range(len(keyListForDiskConfig)):
            append_dataframe_given_values(keyListForDiskConfig[t], str(diskConfigOfVms[t]), isDeletedValueForAppend,
                                          versionForAppend, createdDateForAppend, IdListForDiskConfig[t],
                                          virtualizationEnvironmentType, virtualizationEnvironmentIp, node,
                                          f"api2/extjs/nodes/{node}/qemu/{IdListForIpConfig[t]}/agent/get-fsinfo")


        keyListForOsConfig, osConfigOfVms, IdListFromOsConfig = get_os_info_proxmox.get_os_information(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)

        for t in range(len(keyListForOsConfig)):
            append_dataframe_given_values(keyListForOsConfig[t], str(osConfigOfVms[t]), isDeletedValueForAppend,
                                          versionForAppend, createdDateForAppend, IdListFromOsConfig[t],
                                          virtualizationEnvironmentType, virtualizationEnvironmentIp, node,
                                          "api2/extjs/nodes/"+node+"/qemu/"+str(IdListFromOsConfig[t])+"/agent/get-osinfo")


    dataFrameForInsert.to_sql("proxmox_disc", engineForPostgres, chunksize=5000, index=False, method=None,
                              if_exists='append')
