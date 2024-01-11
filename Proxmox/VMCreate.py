import requests

def create_vm_with_proxmoxer(headers, vmname,id, copiedVmID):

    # getresponseforapis = requests.post("https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu", headers=headersWithCookie, verify=False, json=vm_config)
    clone_info = {
        "newid": int(id),
        "node": "nestedproxmox01",
        "vmid": int(copiedVmID),
        "description": vmname,
        "full": 1,
        "name": vmname,
        "pool": "PM_Pool",
        # "snapname": "ydk01",
        "target": "nestedproxmox01",
        "storage": "Datastore01",
    }
    cloneGivenVm = requests.post("https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/"+str(copiedVmID)+"/clone",headers=headers, verify=False, json=clone_info)
    postVM = {
        "command": 'powershell.exe -command "Initialize-Disk -Number 2 -PartitionStyle MBR"'
    }
    # requests.post(
    #     "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/117/agent/exec", headers=headers,
    #     verify=False, json={
    #     "command": "cmd.exe /c echo select disk 2 > C:\\Users\\Administrator\\diskpart_commands.txt && echo clean >> C:\\Users\\Administrator\\diskpart_commands.txt && echo create partition primary >> C:\\Users\\Administrator\\diskpart_commands.txt && echo assign letter=G >> C:\\Users\\Administrator\\diskpart_commands.txt && echo format fs=ntfs label=Glass_House_Disk quick >> C:\\Users\\Administrator\\diskpart_commands.txt && echo exit >> C:\\Users\\Administrator\\diskpart_commands.txt && start /wait diskpart /s C:\\Users\\Administrator\\diskpart_commands.txt && del diskpart_commands.txt"
    # })

def create_vm_with_esxi():
    print(1)