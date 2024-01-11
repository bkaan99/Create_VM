import base64
import requests
import psycopg2
import pandas as pd
import sys
from sqlalchemy import create_engine
import VMCreate
import startIaaSVM
import updateIaaSVM
import time
import addDiskToIaaS
import assignIpToIaasVm


def createIaasVM(headers, vmListConfig_VmName,id, vmIDForCopyTemplate):
    VMCreate.create_vm_with_proxmoxer(headers, vmListConfig_VmName,id, vmIDForCopyTemplate)

def updateIaasVM():
    updateIaaSVM.update_proxmox_vm(headersWithCookie,vmListConfig_Cpu,vmListConfig_RamSize,vmFirstDiskConfig_DiskSize, vmListConfig_Id,vmListConfig_IpAdress, vmFirstDiskConfig_DiskType, vmFirstDiskConfig_VmDiskImagePath)

def startIaasVM():
    apipath = "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/"+str(vmListConfig_Id+100)+"/status/start"
    startIaaSVM.start_proxmox_vm(apipath, headersWithCookie, vmListConfig_Id+100)

def stopIaasVM():
    apipath = "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/"+str(vmListConfig_Id+100)+"/status/stop"
    startIaaSVM.start_proxmox_vm(apipath, headersWithCookie, vmListConfig_Id+100)

def attachDiskToIaaSVm():
    addDiskToIaaS(vmListConfig_Id,headersWithCookie,numberOfDisks,vmFirstDiskConfig_DiskSize)


if __name__ == "__main__":
    memory = 1024

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
    for vmid in vmIdList:
        VmListConfigrurationTable=pd.read_sql_query("select * from kr_vm_list where id=" + str(vmid), connectionForPostgres)
        VmFirstDiskConfigurationTable=pd.read_sql_query("select * from kr_vm_first_disk where vmlist_id=" + str(vmid), connectionForPostgres)
        numberOfDisks = len(VmFirstDiskConfigurationTable)
        vmListConfig_Id = VmListConfigrurationTable.get("id")[0]
        vmListConfig_Cpu = VmListConfigrurationTable.get("cpu")[0]
        vmListConfig_RamSize = VmListConfigrurationTable.get("ramsizegb")[0]
        #vmListConfig_RamSize = 1
        vmListConfig_VmName = VmListConfigrurationTable.get("vmname")[0]
        vmListConfig_HostName = VmListConfigrurationTable.get("hostname")[0]
        vmListConfig_IpAdress = VmListConfigrurationTable.get("ipaddress")[0]
        vmListConfig_Environment = VmListConfigrurationTable.get("environment")[0]
        vmListConfig_OperatingSystemInformation = VmListConfigrurationTable.get("operatingsysteminformation")[0]
        vmListConfig_OperatingSystemVersion = VmListConfigrurationTable.get("operatingsystemversion")[0]
        vmListConfig_InternetConnection = VmListConfigrurationTable.get("internetconnection")[0]
        vmListConfig_VirtualizationTechnology = VmListConfigrurationTable.get("virtualizationtechnology")[0]
        vmListConfig_PFMSConfigurationId = VmListConfigrurationTable.get("pfmsconfiguration_id")[0]
        #vmListConfig_IsoImagePath = VmListConfigrurationTable.get("iso_location")[0]
        #Fist Disk Alanı
        vmListConfig_RamSize = int(vmListConfig_RamSize) * memory
        vmFirstDiskConfig_Id = VmFirstDiskConfigurationTable.get("id")[0]
        vmFirstDiskConfig_DiskByte = VmFirstDiskConfigurationTable.get("diskbyte")[0]
        vmFirstDiskConfig_DiskSize = VmFirstDiskConfigurationTable.get("disksize")[0]
        vmFirstDiskConfig_VmListId = VmFirstDiskConfigurationTable.get("vmlist_id")[0]
        vmFirstDiskConfig_VmDiskImagePath = VmFirstDiskConfigurationTable.get("location")[0]
        vmFirstDiskConfig_DiskType = VmFirstDiskConfigurationTable.get("controllerlocation")[0]
        #vmFirstDiskConfig_DataStore_Location =
        login = {
            "username": "root",
            "password": "Aa112233!",
            "realm": "pam",
            "new-format": 1
        }
        headers = {
            "Content-Type": "application/json",
        }
        responseforticket = requests.post("https://10.14.46.11:8006/api2/extjs/access/ticket", headers=headers,json=login, verify=False)
        headersWithCookie = {
            "Content-Type": "application/json",
            "Cookie": "PVEAuthCookie=" + responseforticket.json().get("data").get("ticket"),
            "Csrfpreventiontoken": responseforticket.json().get("data").get("CSRFPreventionToken"),
        }

        vmIDForCopyTemplate = 114
        if vmListConfig_OperatingSystemVersion == "Windows 2018 ":
            vmIDForCopyTemplate = 114
        elif vmListConfig_OperatingSystemVersion =='Linux':
            vmIDForCopyTemplate = 102
        createIaasVM(headersWithCookie, vmListConfig_VmName,vmListConfig_Id+100, vmIDForCopyTemplate)
        time.sleep(300)
        updateIaasVM()
        startIaasVM()
        assignIpToIaasVm.assign_ip_to_proxmox_iaas_vm(headersWithCookie,vmid, vmListConfig_IpAdress, "255.255.255.0", "10.14.46.1", "nestedproxmox01", vmListConfig_OperatingSystemVersion)
