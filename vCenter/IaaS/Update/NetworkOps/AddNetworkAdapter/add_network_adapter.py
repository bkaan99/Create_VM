from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *


def get_available_unit_number(vm, max_unit_number=10):
    existing_adapters = [d for d in vm.config.hardware.device if isinstance(d, vim.vm.device.VirtualEthernetCard)]
    used_unit_numbers = {adapter.unitNumber for adapter in existing_adapters}

    # Mevcut adaptör birim numaralarının dışında kullanılabilir birim numaralarını oluştur
    available_unit_numbers = set(range(max_unit_number + 1)) - used_unit_numbers

    # Eğer kullanılabilir birim numarası yoksa, sıradaki birim numarasını kullan
    if not available_unit_numbers:
        next_unit_number = max(used_unit_numbers) + 1
        # Eğer sıradaki birim numarası sınırları aşıyorsa, hata döndür
        if next_unit_number > max_unit_number:
            raise ValueError("Mevcut birim numaraları sınırları aşıyor.")
        available_unit_numbers.add(next_unit_number)

    return min(available_unit_numbers) + 1

def get_next_available_key(vm):
    existing_keys = [device.key for device in vm.config.hardware.device]
    if existing_keys:
        return max(existing_keys) + 1
    else:
        return 0  # veya istediğiniz başka bir pozitif değer

def get_all_networks(content):
    network_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Network], True)
    networks = network_view.view
    return networks

# ...
def get_next_available_device_index(vm):
    existing_devices = [device.deviceInfo.label for device in vm.config.hardware.device if device.deviceInfo]
    # Örnek olarak, mevcut cihaz endekslerini yazdırabilirsiniz:
    print("Mevcut Cihaz Endeksleri:", existing_devices)

    # Yeni bir cihaz endeksi belirleme
    next_device_index = 0
    while f"Network adapter {next_device_index}" in existing_devices:
        next_device_index += 1

    return next_device_index

def add_network_adapter(vm, content, network_name):
    try:
        # Eğer ağ adaptörü zaten varsa eklemeyi atla
        if check_network_adapter_existence(vm, content, network_name):
            print(f"Ağ adaptörü zaten var: {network_name}")
            return

        # Değişiklikleri belirtmek için bir VimVMConfigSpec nesnesi oluşturun
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = []

        # Yeni ağ adaptörü ekleyin
        new_adapter_spec = vim.vm.device.VirtualDeviceSpec()
        new_adapter_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

        # Yeni ağ adaptörü oluşturun (E1000e kullanılıyor)
        new_adapter_spec.device = vim.vm.device.VirtualE1000e()
        new_adapter_spec.device.key = get_next_available_key(vm)

        # Yeni ağ adaptörüne ağ bağlayın
        network = get_network_by_name(content, network_name)
        if network:
            new_adapter_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            new_adapter_spec.device.backing.network = network
            new_adapter_spec.device.backing.deviceName = network_name
        else:
            raise ValueError(f"Ağ '{network_name}' bulunamadı.")

        # Yeni birim numarasını alın
        new_adapter_spec.device.unitNumber = get_next_available_device_index(vm)

        new_adapter_spec.device.deviceInfo = vim.Description()
        new_adapter_spec.device.deviceInfo.label = f"Network adapter {new_adapter_spec.device.unitNumber}"

        # Yeni ağ adaptörünü ekleyin
        spec.deviceChange.append(new_adapter_spec)

        # Değişiklikleri uygulamak için ReconfigVM_Task'i çağırın
        task = vm.ReconfigVM_Task(spec=spec)
        WaitForTask(task)

        print(f"Ağ adaptörü başarıyla eklendi: {network_name}")

    except Exception as e:
        print(f"Ağ adaptörü ekleme hatası: {e}")

def get_network_by_name(content, network_name):
    all_networks = get_all_networks(content)
    for network in all_networks:
        if network.name == network_name:
            return network
    return None

def check_network_adapter_existence(vm, content, network_name):
    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualEthernetCard) and device.deviceInfo.label == network_name:
            return True
    return False

def WaitForTask(task):
    task_done = False
    while not task_done:
        if task.info.state == "success":
            return task.info.result
        if task.info.state == "error":
            print("Hata: ", task.info.error)
            task_done = True

def main(vm_name_to_reconfigure, vCenter_host_ip, vCenter_user, vCenter_password):
    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # VM açık durumdaysa kapat
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM kapatılıyor...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    # Yeni ağ adaptörü ekleyin
    new_network_name = "VM Network"
    add_network_adapter(vm_to_reconfigure, content, new_network_name)

    # VM kapalı durumdaysa aç
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        print("VM açılıyor...")
        task = vm_to_reconfigure.PowerOnVM_Task()
        WaitForTask(task)

    Disconnect(service_instance)
