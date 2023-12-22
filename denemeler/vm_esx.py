import requests
from requests.auth import HTTPBasicAuth
import json

# ESXi host bilgileri
esxi_host = "https://10.14.45.11/ui/#/login"
username = "root"
password = "Aa112233!"

# VM listesi almak için ESXi REST API endpoint'i
api_url = f"{esxi_host}/rest/vcenter/vm"

# HTTP isteği yapmak için gerekli başlıklar
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# ESXi REST API'ye istek yapacak fonksiyon
def make_request(url, method='GET', payload=None):
    auth = HTTPBasicAuth(username, password)
    try:
        response = requests.request(method, url, headers=headers, auth=auth, data=json.dumps(payload), verify=False)
        response.raise_for_status()  # Hata durumunda istisna oluştur
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Error:",err)
    return None

# Tüm VM'lerin detaylarını almak için istek yapma
response_data = make_request(api_url)

# Her VM için detayları yazdırma
if response_data:
    for vm in response_data.get('value', []):
        vm_id = vm['vm']
        vm_details_url = f"{esxi_host}/rest/vcenter/vm/{vm_id}"
        vm_details = make_request(vm_details_url)

        # VM detaylarını yazdırma
        if vm_details:
            print(f"VM Name: {vm_details['value']['name']}")
            print(f"VM Power State: {vm_details['value']['power_state']}")
            print(f"VM CPU Count: {vm_details['value']['cpu_count']}")
            print(f"VM Memory Size: {vm_details['value']['memory_size_MiB']} MiB")
            print("\n")
