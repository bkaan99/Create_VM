import requests


def add_disk_to_proxmox_iaas_vm(vmid,headersWithCookie,numberOfDisk,diskSize):
    add_disk_config={
        "ide" + numberOfDisk + "": "Datastore01:"+diskSize
    }
    addDiskToVm = requests.put(
        "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/" + str(vmid + 100) + "/config",
        headers=headersWithCookie, verify=False, json=add_disk_config)

def add_disk_to_esxi_iaas_vm(vmid,headersWithCookie,numberOfDisk):
    print(1)