from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def delete_last_network_adapter(vm, content):
    try:
        # Mevcut ağ adaptörlerini alın
        existing_adapters = [device for device in vm.config.hardware.device if isinstance(device, vim.vm.device.VirtualEthernetCard)]

        # Eğer hiç ağ adaptörü yoksa işlemi atla
        if not existing_adapters:
            print("Silinecek ağ adaptörü bulunamadı.")
            return

        # En son oluşturulan adaptörü bulun
        last_created_adapter = max(existing_adapters, key=lambda x: x.key)

        # Değişiklikleri belirtmek için bir VimVMConfigSpec nesnesi oluşturun
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = []

        # Silinecek ağ adaptörünü silmek için bir VirtualDeviceSpec nesnesi oluşturun
        delete_adapter_spec = vim.vm.device.VirtualDeviceSpec()
        delete_adapter_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
        delete_adapter_spec.device = last_created_adapter

        # Silme işlemini değişikliklere ekleyin
        spec.deviceChange.append(delete_adapter_spec)

        # Değişiklikleri uygulamak için ReconfigVM_Task'i çağırın
        task = vm.ReconfigVM_Task(spec=spec)
        WaitForTask(task)

        print(f"Ağ adaptörü başarıyla silindi: {last_created_adapter.deviceInfo.label}")

    except Exception as e:
        print(f"Ağ adaptörü silme hatası: {e}")

def WaitForTask(task):
    task_done = False
    while not task_done:
        if task.info.state == "success":
            return task.info.result
        if task.info.state == "error":
            print("Hata: ", task.info.error)
            task_done = True

def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    vm_name_to_reconfigure = "bkaan_deneme"

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # VM açık durumdaysa kapat
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM kapatılıyor...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    # En son oluşturulan ağ adaptörünü silin
    delete_last_network_adapter(vm_to_reconfigure, content)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
