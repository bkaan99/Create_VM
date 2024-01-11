import requests

def add_new_disk_to_iaas_vm(headersWithCookie,disksize,diskTypeAndNumber,vmid,dataStore):
    headersWithCookie = {
        "Content-Type": "application/json",
        "Cookie": "PVEAuthCookie=" + "PVE%3Aroot@pam%3A659E8770%3A%3AeFs9jZoEUeexsETS70sTkCyae/AxRuyGGIGtOrgI+XzusLr51x6aQBb9Y+I4NkDNo5VnpaJpxcrnvt3yaS4rTzGQuElSV3l+A4kydTJlWgjfxXImo/ylgd92jtTi/S5V98auU/VuXEVkAakjXqcFKbRlFzOy9XpGpPQPu6zLXBa84BFhAlqCLSoBvKe+c5kDuv9xZJ3Um/FqHc1dLCavkOZLYbIez5zTOEXng+G0kE4PvBGdm0vqezcdSaRu7j6fZFM4DF6YIN7alvJJ/Izgq9X2i0Z010xp/kGi+eU/VCVtx1MvhUfhakNQwKh8zk0Q8Om5GBFncW3BUmH6rrfFPQ%3D%3D",
        "Csrfpreventiontoken": "659E8770:symIyWQ6bTCuJXv6HEFxvg9hFoyYdokm0tLM2+PFN00",
    }

    # addDiskConfig = {
    #     diskTypeAndNumber:dataStore+":"+str(disksize)
    # }

    command = [
        "touch /deneme.sh",
        "chmod 777 /deneme.sh",
        "/process_command.sh echo \"123\"",
        "/process_command.sh sudo su",
        "/process_command.sh sudo mkdir /mnt/mythi30",
        "/process_command.sh sudo parted /dev/sdb mklabel gpt",
        "/process_command.sh sudo parted /dev/sdb mkpart primary ext4 0% 100%",
        "/process_command.sh sudo parted /dev/sdb quit",
        "/process_command.sh sudo mkfs.ext4 /dev/sdb1",
        "/process_command.sh echo \"/dev/sdb1 /mnt/mythi30 ext4 defaults 0 0\" | tee -a /etc/fstab",
        "/process_command.sh sudo systemctl daemon-reload",
        "/process_command.sh sudo mount -a /mnt/mythi30",
        "/process_command.sh exit"
    ]


##  "/process_command.sh sudo su",
    ##    "/process_command.sh echo \"123\"",


    for i in command:
        postVM = {
            "command": i,
            "vmid": "131",
            "node": "nestedproxmox01"
        }
        setDiskSize = requests.post(
            "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/131/agent/exec",
            headers=headersWithCookie, verify=False, json=postVM)



    requests.post(
        "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/131/agent/exec",
        headers=headersWithCookie, verify=False, json={
            "command": "./deneme.sh -y",
            "vmid": "131",
            "node": "nestedproxmox01"
        })


def main():
    add_new_disk_to_iaas_vm("headersWithCookie", 10, "scsi1", "131", "Datastore01")

if __name__ == '__main__':
    main()

