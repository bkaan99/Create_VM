
def proxmox_credential():
    proxmox_login = {
            "username": "root",
            "password": "Aa112233!",
            "realm": "pam",
            "new-format": 1
        }

    virtualizationEnvironmentIp = "10.14.46.11:8006"

    return proxmox_login, virtualizationEnvironmentIp

def ipam_credential():
    ipam_login = {
        "username": "ansible",
        "password": "Cekino123!"
    }

    ipam_api_url = "https://172.28.0.27/api/0002/"

    ipam_base_url = "172.28.0.27"

    return ipam_login, ipam_api_url, ipam_base_url