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

def itsm_credential():

    itsm_login = {
        "username" : "cekinoitsmuser",
        "password" : "Cekino123!!"
    }

    itsm_api_url = "https://supporttest.glasshouse.com.tr/api/v3"
    itsm_api_key = "A919767F-C901-4874-B0D4-0D3EE04CD3F2"

    return  itsm_api_url, itsm_api_key

def vcenter_credential():
    login_credential = {
        "host_ip": "10.14.45.10",
        "username": "cekinoitsmuser",
        "password": "Cekino123!!"
    }

    return login_credential




