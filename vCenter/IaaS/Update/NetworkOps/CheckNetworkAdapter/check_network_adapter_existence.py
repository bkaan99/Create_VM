import time
from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

def get_all_networks(content):
    network_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Network], True)
    networks = network_view.view
    return networks

def check_any_network_adapter_existence(vm):
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualEthernetCard):
            device_label = device.deviceInfo.label
            return True, device_label
    return False, None

def WaitForTask(task):
    task_done = False
    while not task_done:
        if task.info.state == "success":
            return task.info.result
        if task.info.state == "error":
            print("Hata: ", task.info.error)
            task_done = True
        time.sleep(1)  # 1 saniye bekleyerek tekrar kontrol et

def main(vCenter_host_ip, vCenter_user, vCenter_password, vm_name):

    service_instance, content = create_vsphere_connection(host=vCenter_host_ip, user=vCenter_user, password=vCenter_password)

    vm_to_reconfigure = get_vm_by_name(content, vm_name)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name} bulunamadı.")
        Disconnect(service_instance)
        return

    # Ağ adaptörü varlığı kontrolü ve label bilgisi
    network_adapter_existence_value, device_label = check_any_network_adapter_existence(vm_to_reconfigure)

    if network_adapter_existence_value:
        print(f"Ağ adaptörü '{device_label}' VM'de bulunuyor.")
    else:
        print("Ağ adaptörü VM'de bulunmuyor.")

    Disconnect(service_instance)

    return network_adapter_existence_value, device_label

if __name__ == "__main__":
    main()
