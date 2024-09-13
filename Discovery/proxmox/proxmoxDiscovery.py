import requests
import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, DateTime, MetaData, inspect, Boolean, Integer
from datetime import datetime
from Discovery import Credentials
from Discovery.proxmox.utils import get_disk_volumes_proxmox, get_ip_information_proxmox, get_nodes_proxmox, \
    get_host_name_proxmox, get_vm_id_list_proxmox, get_vm_config_proxmox, get_os_info_proxmox


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    #dataFrameForInsert._append(pd.DataFrame([key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes],columns=dataFrameForInsert.columns,ignore_index=True))
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

# def appaend_dataframe_for_pool_table(vmid,vm_name,pool_name,is_deleted,created_date,version,virtualization_environment_type,virtualization_environment_ip,customer_name,is_matched,vm_type,vm_note):
#     dataFrameForInsertPoolTable.loc[len(dataFrameForInsertPoolTable)]=[vmid,vm_name,pool_name,is_deleted,created_date,version,virtualization_environment_type,virtualization_environment_ip,customer_name,is_matched,vm_type,vm_note]

def get_node_information_from_json(jsonWithNodes):
    listOfNodeNames = []
    for i, item in enumerate(jsonWithNodes):
        listOfNodeNames.append(item["node"])
    return listOfNodeNames

def discover_proxmox_environment(nodeName):
    url = f"https://{virtualizationEnvironmentIp}/api2/extjs/nodes/"+nodeName+"/qemu"
    discoveredNodeData = get_vm_id_list_proxmox.get_vm_id_list(headersWithCookie, url)
    return discoveredNodeData
def get_id_from_discovered_data(firstDiscoveredJson):
    listOfVMIDS = []
    for i, item in enumerate(firstDiscoveredJson):
        listOfVMIDS.append(item["vmid"])
    return listOfVMIDS

def append_vm_info(vmID, key, value, additional_info='', nodeNametoInsert=''):
    try:
        append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, virtualizationEnvironmentIp, nodeName= nodeNametoInsert,
                                      notes=f"{str(additional_info)}")
    except:
        pass

def extract_useful_data_from_vm_config(configList,nodenameToInsert):
    for c, config in enumerate(configList):
        keysOfConfig = config.keys()
        for key in keysOfConfig:
            listOfValuesForDataFrame = []
            if "acpi" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["acpi"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "affinity" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["affinity"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)
            elif "agent" in key:
                #@TODO Will be changed later!!! (only one data for agent active/passive data found)
                keyForInsert = key
                valueForInsert = config["agent"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)
            elif "arch" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["arch"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "args" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["args"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "audio0" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["audio0"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "autostart" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["autostart"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "balloon" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["balloon"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "bios" == key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["bios"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "boot" == key:
                keyForInsert = key
                valueForInsert = config["boot"]
                notes = valueForInsert
                try:
                    for t in range(len(valueForInsert.split("=")[1].split(";"))):
                        insertSplittedValue = valueForInsert.split("=")[1].split(";")[t]
                        append_vm_info(IdList[c], keyForInsert, insertSplittedValue, notes, nodenameToInsert)

                except:
                        insertSplittedValue = valueForInsert
                        append_vm_info(IdList[c], keyForInsert, insertSplittedValue, notes, nodenameToInsert)

            elif "bootdisk" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["bootdisk"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cdrom" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["cdrom"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cicustom" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["cicustom"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ciuser" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["ciuser"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cipassword" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["cipassword"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "citype" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["citype"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ciupgrade" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["ciupgrade"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ciuser" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["ciuser"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cores" in key:
                keyForInsert = key
                valueForInsert = config["cores"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cpu" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["cpu"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cpulimit" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["cpulimit"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "cpuunits" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["cpuunits"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "description" in key:
                keyForInsert = key
                valueForInsert = config["description"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "digest" in key:
                keyForInsert = key
                valueForInsert = config["digest"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "efidisk0" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["efidisk0"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "freeze" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["freeze"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "hookscript" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["hookscript"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "hostpci" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["hostpci"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "hotplug" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["hotplug"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "hugepages" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["hugepages"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ide" in key:
                #@TODO Might be edited for different ide results!!
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

                except:
                    insertSplittedValue = valueForInsert
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ipconfig" in key:
                #@TODO Might be edited for different ipconfig results!!
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                try:
                    insertSplittedValue = valueForInsert.replace(",","|")
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

                except:
                    insertSplittedValue = valueForInsert
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ivshmem" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["ivshmem"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "keephugepages" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["keephugepages"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "keyboard" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["keyboard"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "kvm" in key:
                keyForInsert = key
                valueForInsert = config["kvm"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "localtime" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["localtime"]
                notes = valueForInsert
                append_dataframe_given_values(keyForInsert, valueForInsert, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, IdList[c], virtualizationEnvironmentType,
                                              virtualizationEnvironmentIp, nodenameToInsert, notes)
            elif "lock" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["lock"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "machine" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["machine"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "memory" in key:
                keyForInsert = key
                valueForInsert = config["memory"]
                notes = valueForInsert
                append_dataframe_given_values(keyForInsert, int(valueForInsert)/1024, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, IdList[c], virtualizationEnvironmentType,
                                              virtualizationEnvironmentIp, nodenameToInsert, notes)
            elif "migrate_downtime" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["migrate_downtime"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "migrate_speed" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["migrate_speed"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "name" in key:
                keyForInsert = key
                valueForInsert = config["name"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "nameserver" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config["nameserver"]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "net" in key:
                #@TODO Will be changed later!!! (got only limited data for net[n])
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                try:
                    valueForInsert = valueForInsert.replace(",","|")
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

                except:
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "numa" == key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "numa" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "onboot" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "ostype" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "parallel" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "protection" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "reboot" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "rng0" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "sata" in key:
                #@TODO Might be edited for different sata results!!
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

                except:
                    insertSplittedValue = valueForInsert
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "scsihw" == key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "scsi" in key:
                #@TODO Might be edited for different scsi results!!
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

                except:
                    insertSplittedValue = valueForInsert
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "searchdomain" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "serial" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "shares" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "smbios1" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "smp" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "sockets" in key:
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "spice_enhancement" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "sshkeys" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "startdate" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "startup" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "tablet" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "tags" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "tdf" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "template" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "tpmstate0" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "unused" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "usb" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "vcpus" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "vga" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "virtio" in key:
                #@TODO Might be edited for different virtio results!!
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                try:
                    insertSplittedValue = valueForInsert.split(":")[0]+"|"+valueForInsert.split(":")[1].split(",")[0]+"|"+valueForInsert.split("size=")[1]+"B"
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

                except:
                    insertSplittedValue = valueForInsert
                    append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "vmgenid" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "vmstatestorage" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            elif "watchdog" in key:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert)

            else:
                #@TODO Will be changed later!!! (no data found in config during tests it will be upgraded when its needed)
                keyForInsert = key
                valueForInsert = config[key]
                notes = valueForInsert
                append_vm_info(IdList[c], keyForInsert, valueForInsert, notes, nodenameToInsert),

def create_datastore_table_if_not_exists(engine, table_name: str):
    metadata = MetaData()
    datastore_table = Table(
        table_name, metadata,
        Column('key', String),
        Column('value', String),
        Column('is_deleted', Boolean),
        Column('version', Integer),
        Column('created_date', DateTime),
        Column('vm_id', Integer),
        Column('virtualization_environment_type', String),
        Column('virtualization_environment_ip', String),
        Column('node', String),
        Column('notes', String)
    )
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        metadata.create_all(engine)
        print(f"{table_name} ---> tablosu oluşturuldu.")
    else:
        print("")
        print(f"{table_name} ---> tablosu zaten var.")

if __name__ == "__main__":
    login_credential, virtualization_ip = Credentials.new_proxmox_credential()
    TABLE_NAME = "kr_discovery_proxmox"

    createdDateForAppend = datetime.now()
    versionForAppend = 1
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "Proxmox"
    virtualizationEnvironmentIp = virtualization_ip

    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)

    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')

    create_datastore_table_if_not_exists(engineForPostgres, TABLE_NAME)

    login = {
            "username": login_credential.get("username"),
            "password": login_credential.get("password"),
            "realm": "pam",
            "new-format": 1
        }
    headers = {
            "Content-Type": "application/json",
        }
    responseforticket = requests.post(f"https://{virtualizationEnvironmentIp}/api2/extjs/access/ticket", headers=headers,json=login, verify=False)
    headersWithCookie = {
            "Content-Type": "application/json",
            "Cookie": "PVEAuthCookie=" + responseforticket.json().get("data").get("ticket"),
            "Csrfpreventiontoken": responseforticket.json().get("data").get("CSRFPreventionToken"),
        }
    urlToGetNodes = "https://"+str(virtualizationEnvironmentIp)+"/api2/json/nodes/"
    nodesOfGivenEnvironment = get_nodes_proxmox.get_nodes(headersWithCookie, urlToGetNodes)
    clearedNodeInfo = get_node_information_from_json(nodesOfGivenEnvironment)
    # poolVmIdList = []
    # poolVmNameList = []
    # poolNameList = []
    # poolTableIsDeletedList = []
    # poolTableCreatedDateList = []
    # poolTableVersionList = []
    # poolTableVirtualizationEnvironmentList = []
    # poolTableVirtualizatonEnvironmentIpList = []
    # poolTableCustomerNameList = []
    # poolTableIsMatchedValueList = []
    # poolTableVmTypeList = []
    # poolTableNoteList = []
    # poolTableColumns = ["vmid","vm_name","pool_name","is_deleted","created_date","version","virtualization_environment_type","virtualization_environment_ip","customer_name","is_matched","vm_type","vm_note"]
    # dataFrameForInsertPoolTable = pd.DataFrame(columns=poolTableColumns)
    # poolData = get_pool_info.get_pool_names(headersWithCookie)
    # for poolname in poolData:
    #     poolInfoList = get_pool_information.get_pool_information(headersWithCookie, poolname)
    #     for object in poolInfoList["members"]:
    #         poolNameList.append(poolname)
    #         poolVmNameList.append(object.get("name"))
    #         poolVmIdList.append(object.get("vmid"))
    #         poolTableIsDeletedList.append(isDeletedValueForAppend)
    #         poolTableCreatedDateList.append(createdDateForAppend)
    #         poolTableVersionList.append(versionForAppend)
    #         poolTableVirtualizationEnvironmentList.append(virtualizationEnvironmentType)
    #         poolTableVirtualizatonEnvironmentIpList.append(virtualizationEnvironmentIp)
    #         poolTableCustomerNameList.append(None)
    #         poolTableIsMatchedValueList.append(False)
    #         poolTableVmTypeList.append(None)
    #         poolTableNoteList.append(None)
    # for i in range(len(poolVmIdList)):
    #     appaend_dataframe_for_pool_table(poolVmIdList[i], poolVmNameList[i], poolNameList[i], poolTableIsDeletedList[i], poolTableCreatedDateList[i], poolTableVersionList[i], poolTableVirtualizationEnvironmentList[i], poolTableVirtualizatonEnvironmentIpList[i],poolTableCustomerNameList[i],poolTableIsMatchedValueList[i],poolTableVmTypeList[i],poolTableNoteList[i])
    # dataFrameForInsertPoolTable.to_sql("kr_pool_info", engineForPostgres, chunksize=5000, index=False, method=None,if_exists='append')

    for node in clearedNodeInfo:
        discoveredNodeData = discover_proxmox_environment(node)
        listOfVMIDS = get_id_from_discovered_data(discoveredNodeData)
        configListOfVms, IdList = get_vm_config_proxmox.get_vm_config(headersWithCookie, listOfVMIDS, node, virtualizationEnvironmentIp)

        extract_useful_data_from_vm_config(configListOfVms,node)
        keyListForIpConfig, ipconfigsOfVms, IdListForIpConfig = get_ip_information_proxmox.get_ip_given_vm(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)
        keyListForDiskConfig, diskConfigOfVms, IdListForDiskConfig = get_disk_volumes_proxmox.get_disk_information(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)
        keyListForOsConfig, osConfigOfVms, IdListFromOsConfig = get_os_info_proxmox.get_os_information(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)
        keyListForHostConfig, hostConfigOfVms, IdListFromHostConfig = get_host_name_proxmox.get_host_name(virtualizationEnvironmentIp, node, listOfVMIDS, headersWithCookie)

        for t, item in enumerate(keyListForIpConfig):
            append_dataframe_given_values(item, str(ipconfigsOfVms[t]), isDeletedValueForAppend, versionForAppend, createdDateForAppend, IdListForIpConfig[t], virtualizationEnvironmentType, virtualizationEnvironmentIp, node, str(ipconfigsOfVms[t]))
        for t, item in enumerate(keyListForDiskConfig):
            append_dataframe_given_values(item, str(diskConfigOfVms[t]), isDeletedValueForAppend, versionForAppend, createdDateForAppend, IdListForDiskConfig[t], virtualizationEnvironmentType, virtualizationEnvironmentIp, node, str(diskConfigOfVms[t]))
        for t, item in enumerate(keyListForOsConfig):
            append_dataframe_given_values(item, str(osConfigOfVms[t]), isDeletedValueForAppend, versionForAppend, createdDateForAppend, IdListFromOsConfig[t], virtualizationEnvironmentType, virtualizationEnvironmentIp, node, str(osConfigOfVms[t]))
        for t, item in enumerate(keyListForHostConfig):
            append_dataframe_given_values(item, str(hostConfigOfVms[t]), isDeletedValueForAppend, versionForAppend, createdDateForAppend, IdListFromHostConfig[t], virtualizationEnvironmentType, virtualizationEnvironmentIp, node, str(hostConfigOfVms[t]))


        dataFrameForInsert.to_sql(TABLE_NAME, engineForPostgres, chunksize=5000, index=False, method=None,
                   if_exists='replace')
