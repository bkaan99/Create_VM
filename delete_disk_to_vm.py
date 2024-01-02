from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def get_last_used_unit_number(vm):
    existing_disks = [d for d in vm.config.hardware.device if isinstance(d, vim.VirtualDisk)]
    if existing_disks:
        return max([disk.unitNumber for disk in existing_disks])
    else:
        return -1  # Eğer disk yoksa, -1 döndür

def get_available_unit_number(vm, max_unit_number=15):
    existing_disks = [d for d in vm.config.hardware.device if isinstance(d, vim.VirtualDisk)]
    used_unit_numbers = {disk.unitNumber for disk in existing_disks}

    # Mevcut disk birim numaralarının dışında kullanılabilir birim numaralarını oluştur
    available_unit_numbers = set(range(max_unit_number + 1)) - used_unit_numbers

    # Eğer kullanılabilir birim numarası yoksa, sıradaki birim numarasını kullan
    if not available_unit_numbers:
        next_unit_number = max(used_unit_numbers) + 1
        # Eğer sıradaki birim numarası sınırları aşıyorsa, hata döndür
        if next_unit_number > max_unit_number:
            raise ValueError("Mevcut birim numaraları sınırları aşıyor.")
        available_unit_numbers.add(next_unit_number)

    return min(available_unit_numbers)

def delete_disk_by_name(vm, disk_name):
    try:
        # Silinecek disk adına sahip bir disk bulun
        disk_to_remove = None
        for device in vm.config.hardware.device:
            if isinstance(device, vim.VirtualDisk) and device.deviceInfo.label == disk_name:
                disk_to_remove = device
                break

        if disk_to_remove is None:
            raise ValueError(f"{disk_name} adına sahip bir disk bulunamadı.")

        # Diski kaldırmak için bir VimVMConfigSpec nesnesi oluşturun
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = [vim.VirtualDeviceConfigSpec(device=disk_to_remove, operation=vim.vm.device.VirtualDeviceSpec.Operation.remove)]

        # Değişiklikleri uygulamak için ReconfigVM_Task'i çağırın
        task = vm.ReconfigVM_Task(spec=spec)
        WaitForTask(task)

        print(f"{disk_name} adına sahip disk başarıyla kaldırıldı.")
    except Exception as e:
        print(f"Disk kaldırma hatası: {e}")

# ...
def WaitForTask(task):
    """Bir vSphere görevi tamamlanana kadar bekler ve güncellemeler sağlar."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Görev başarıyla tamamlandı.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Hata: {task.info.error}")
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

    vm_name_to_reconfigure = "yeni_bkaan_cemo"

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # VM açık durumdaysa kapat
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM kapatılıyor...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    # Silinecek disk adı
    disk_to_remove_name = "Hard disk 2"  # Silinecek disk adını değiştirin
    delete_disk_by_name(vm_to_reconfigure, disk_to_remove_name)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
