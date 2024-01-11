import requests

def stop_proxmox_vm(apipath, headersWithCookie, vmId,nodename):
    nodename = "nestedproxmox01"
    start_vm = {
        "vmid": int(vmId),
        "node": nodename
    }
    startVmResponse = requests.post(apipath,headers=headersWithCookie, verify=False, json=start_vm)
