import requests
import json

def get_vcenter_session(vcenter_host, vcenter_user, vcenter_password):
    url = f"https://{vcenter_host}/rest/com/vmware/cis/session"
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": vcenter_user,
        "password": vcenter_password
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    if response.status_code == 200:
        return response.json()["value"]
    else:
        print(f"Failed to get vCenter session: {response.text}")
        return None

def power_on_vm(vcenter_host, session_id, vm_name):
    url = f"https://{vcenter_host}/rest/vcenter/vm/{vm_name}/power/start"
    headers = {
        "Content-Type": "application/json",
        "vmware-api-session-id": session_id
    }
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"{vm_name} powered on successfully.")
    else:
        print(f"Failed to power on {vm_name}: {response.text}")

def main(vm_name_to_power_on, vcenter_host, vcenter_user, vcenter_password):
    session_id = get_vcenter_session(vcenter_host, vcenter_user, vcenter_password)
    if session_id:
        power_on_vm(vcenter_host, session_id, vm_name_to_power_on)

if __name__ == "__main__":
    main("bkaan_deneme", "10.14.45.11", "administrator@vsphere.local", "Aa112233!")
