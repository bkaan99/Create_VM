import time
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl


def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def get_all_networks(content):
    network_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Network], True)
    networks = network_view.view
    return networks

def check_any_network_adapter_existence(vm):
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualEthernetCard):
            device_label = device.deviceInfo.label
            return True, device_label
    return False

def WaitForTask(task):
    task_done = False
    while not task_done:
        if task.info.state == "success":
            return task.info.result
        if task.info.state == "error":
            print("Hata: ", task.info.error)
            task_done = True
        time.sleep(1)  # 1 saniye bekleyerek tekrar kontrol et


def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    vm_name_to_reconfigure = "Clone-SUSE-Temp-15-3"

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        Disconnect(service_instance)
        return

    # VM açık durumdaysa kapat
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM kapatılıyor...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    # Ağ adaptörü varlığı kontrolü ve label bilgisi
    network_adapter_existence, device_label = check_any_network_adapter_existence(vm_to_reconfigure)

    if network_adapter_existence:
        print(f"Ağ adaptörü '{device_label}' VM'de bulunuyor.")
    else:
        print(f"Ağ adaptörü VM'de bulunmuyor.")

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
