
def proxmox_credential():
    login = {
            "username": "root",
            "password": "Aa112233!",
            "realm": "pam",
            "new-format": 1
        }

    virtualizationEnvironmentIp = "10.14.46.11:8006"

    return login, virtualizationEnvironmentIp

