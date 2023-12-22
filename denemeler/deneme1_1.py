import requests
from requests.auth import HTTPBasicAuth

# ESXi host bilgileri
esxi_host = "10.14.45.11"
username = "root"
password = "Aa112233!"

# vSphere REST API endpoint
api_url = f"https://{esxi_host}"

# API isteği için gerekli başlık
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# API'ye yapılan istek için kimlik doğrulama
auth = HTTPBasicAuth(username, password)

# Sanal makineleri almak için bir istek yap
response = requests.get(f"{api_url}/ui/i18n/en_US/vm.txt", headers=headers, auth=auth, verify=False)

# Yanıtı kontrol et
if response.status_code == 200:
    vms_info = response.json()
    print("Sanal Makineler:")
    for vm in vms_info['value']:
        print(f"VM ID: {vm['vm']} - VM Adı: {vm['name']}")
else:
    print(f"Hata: {response.status_code}, {response.text}")
