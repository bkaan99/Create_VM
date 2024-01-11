import requests

def update_proxmox_vm(headersWithCookie, cores, ram, disksize, vmid,vmListConfig_IpAdress, vmdiskConfigDiskType, diskLocation):
    update_config = {
        "cores":int(int(cores)/2),
        "memory":int(ram),
        #"net0":"model=e1000,bridge=vmbr0,firewall=1",
        "kvm":0
}
    if vmdiskConfigDiskType=="SATA":
        numberOfSataDisk = requests.get("https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/"+str(vmid+100)+"/config",headers=headersWithCookie, verify=False).text.count("sata")
        disk_key = "sata"+str(numberOfSataDisk)
    elif vmdiskConfigDiskType=="IDE":
        numberOfSataDisk = requests.get(
            "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/" + str(vmid + 100) + "/config",
            headers=headersWithCookie, verify=False).text.count("ide")-1
        #@TODO Yukarıdaki -1 ibaresi ileride düzeltilecektir
        disk_key = "ide" + str(numberOfSataDisk)

    update_config[disk_key] = diskLocation+":"+str(disksize)
    setIpOnVM = requests.put("https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/"+str(vmid+100)+"/config",
                             headers=headersWithCookie, verify=False, json=update_config)



def update_esxi_vm():
    print(1)