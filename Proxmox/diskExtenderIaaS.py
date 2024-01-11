import requests

def extend_disk_for_proxmox_iaas_vm(headersWithCookie,vmid, nodename, serverOs):
    nodename = "nestedproxmox01" #@TODO Nodaneme generic olacak
    #@TODO Commandler sudoerse göre güncelelenecektir.
    if serverOs == "Windows 2018":
        commandToAddIP = "cmd.exe /c echo select disk 2 > C:\\Users\\Administrator\\diskpart_commands.txt && echo clean >> C:\\Users\\Administrator\\diskpart_commands.txt && echo create partition primary >> C:\\Users\\Administrator\\diskpart_commands.txt && echo assign letter=G >> C:\\Users\\Administrator\\diskpart_commands.txt && echo format fs=ntfs label=Glass_House_Disk quick >> C:\\Users\\Administrator\\diskpart_commands.txt && echo exit >> C:\\Users\\Administrator\\diskpart_commands.txt && start /wait diskpart /s C:\\Users\\Administrator\\diskpart_commands.txt && del diskpart_commands.txt"

    elif serverOs == "Linux":

        commandToDelIP = "our shell command here"

    run_agent_for_disk_extend = {
        "command": commandToAddIP,
        "vmid": vmid,
        "node": nodename
    }

    setDiskSize = requests.post(
        "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/" + str(vmid + 100) + "/agent/exec",
        headers=headersWithCookie, verify=False, json=run_agent_for_disk_extend)