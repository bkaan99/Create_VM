import requests


def run_proxmox_command(headers, node, vmid, command):
    url = f"https://your-proxmox-server:8006/api2/extjs/nodes/{node}/qemu/{vmid}/agent/exec"
    payload = {"command": command, "vmid": vmid, "node": node}
    response = requests.post(url, headers=headers, verify=False, json=payload)
    return response.json()


def main():
    headers = {
        "Content-Type": "application/json",
        "Cookie": "PVEAuthCookie=" + "PVE%3Aroot@pam%3A65AA5014%3A%3APYl1m+1cx1FcG/Q1CTJ6Nzc8noY3IVw7Erg7XR9VITs1lEK0wgJuLnE0qrhJVWrrH17B2eDtCoSvateDU889W5rRjaNVwa4qaHwNQkvSDyQqoMu2BOYvEEZ1nbILCzTxnxI0sWqCx/zxQCVl/scM/5cdR2jLgH6ALPyiEMY7bOfXbbAGf3srmrdYe7/7DZj5uBuEIS49jQRk4P4Y0/Vcc5PS4hiouP14EL7/R94dM7UkvCt1Nmog7l5rvEqtpXpJMsJYQA6NNSLcpygWpmgAsTVSmKgogaWSQnBw1jVwolpd+2wqjQIKPtxF6qFixX3lpm3qpRogi0g3dgV+QAlgbQ%3D%3D",
        "Csrfpreventiontoken": "65AA5014:Vk+CJlcOlioAnjMzjbpqMZcTn2HBDvVX7lJZtn6GrnM"
    }

    # node = "nestedproxmox01"
    # vmid = "124"
    #
    # added_disk_full_path_name = "/dev/sdb"
    # disk_mount_location = "hana/deneme"

    # Disk oluşturma ve bölme
    # command1= f"sudo parted {added_disk_full_path_name} <<EOF\n" \
    #           "mklabel gpt\n" \
    #           "mkpart primary xfs 1MiB 100%\n" \
    #           "quit\n" \
    #           "EOF"
    # run_proxmox_command(headers, node, vmid, command1)
    #
    # # Disk biçimlendirme
    # command2 = f"sudo mkfs.xfs {added_disk_full_path_name}1"
    # run_proxmox_command(headers, node, vmid, command2)
    #
    # # Mount noktası oluşturma
    # command3 = f"sudo mkdir -p /{disk_mount_location}"
    # run_proxmox_command(headers, node, vmid, command3)
    #
    # # /etc/fstab dosyasını düzenleme
    # command4 = f'echo "{added_disk_full_path_name}1 /{disk_mount_location} xfs defaults 0 0" | sudo tee -a /etc/fstab'
    # run_proxmox_command(headers, node, vmid, command4)
    #
    # # Systemd'i yeniden yükleme
    # command5 = "sudo systemctl daemon-reload"
    # run_proxmox_command(headers, node, vmid, command5)
    #
    # # Diski bağlama (mount etme)
    # command6 = f'sudo mount {added_disk_full_path_name}1  /{disk_mount_location}'

    command = [
        "touch /deneme.sh",
        "chmod 777 /deneme.sh",
        "/process_command.sh echo \"123\"",
        "/process_command.sh sudo su",
        "/process_command.sh sudo mkdir -p /mnt/mythi30",
        "/process_command.sh sudo parted /dev/sda mklabel gpt",
        "/process_command.sh sudo parted /dev/sda mkpart primary xfs 1MiB 100%",
        "/process_command.sh sudo parted /dev/sda quit",
        "/process_command.sh sudo mkfs.xfs /dev/sda1",
        "/process_command.sh echo \"/dev/sda1 /mnt/mythi30 xfs defaults 0 0\" | tee -a /etc/fstab",
        "/process_command.sh sudo systemctl daemon-reload",
        "/process_command.sh sudo mount -a /mnt/mythi30",
        "/process_command.sh exit"
    ]

    ##  "/process_command.sh sudo su",
    ##    "/process_command.sh echo \"123\"",

    for i in command:
        postVM = {
            "command": i,
            "vmid": "129",
            "node": "nestedproxmox01"
        }
        requests.post(
            "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/129/agent/exec",
            headers=headers, verify=False, json=postVM)


    requests.post(
        "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/129/agent/exec",
        headers=headers, verify=False, json={
            "command": "./deneme.sh -y",
            "vmid": "131",
            "node": "nestedproxmox01"
        })

    #run_proxmox_command(headers, node, vmid, command6)

if __name__ == '__main__':
    main()



