def proxmox_credential():
    proxmox_login = {
            "username": "root",
            "password": "Aa112233!",
            "realm": "pam",
            "new-format": 1
        }

    virtualizationEnvironmentIp = "10.14.46.11:8006"

    return proxmox_login, virtualizationEnvironmentIp

def new_proxmox_credential():
    proxmox_login = {
            "username": "root",
            "password": "Aa112233!",
            "realm": "pam",
            "new-format": 1
        }

    virtualizationEnvironmentIp = "10.14.45.51:8006"

    return proxmox_login, virtualizationEnvironmentIp

def ipam_credential():
    ipam_login = {
        "username": "ansible",
        "password": "Cekino123!"
    }

    ipam_api_url = "https://172.28.0.27/api/0002/"

    ipam_base_url = "172.28.0.27"

    return ipam_login, ipam_api_url, ipam_base_url
def ipam_live_credential():
    ipam_login = {
        "username": "cekinoIpamUser",
        "password": "WQeMGw725"
    }

    ipam_api_url = "https://172.28.0.17/api/0001/"

    ipam_base_url = "172.28.0.17"

    return ipam_login, ipam_api_url, ipam_base_url

def itsm_credential():

    itsm_login = {
        "username" : "cekinoitsmuser",
        "password" : "Cekino123!!"
    }

    itsm_api_url = "https://supporttest.glasshouse.com.tr/api/v3"
    itsm_api_key = "A919767F-C901-4874-B0D4-0D3EE04CD3F2"

    return itsm_api_url, itsm_api_key
def itsm_live_credential():

    itsm_login = {
        "username" : "cekinoitsmuser",
        "password" : "Aa112233!"
    }

    itsm_api_url = "https://support.glasshouse.com.tr/api/v3"
    itsm_api_key = "72860D48-B48B-444E-8AEB-B527206C31EE"

    return itsm_api_url, itsm_api_key

def vcenter_credential():
    login_credential = {
        "host_ip": "10.14.45.10",
        "username": "administrator@vsphere.local",
        "password": "Aa112233!"
    }

    return login_credential

def turksat_vmware_credential():
    login_credential = {
        "host_ip": "10.184.1.10",
        "username": "P9988.marvin.android@vsphere.local",
        "password": "T7z8nSVChzmzw3zUjK9."

    }

    return login_credential