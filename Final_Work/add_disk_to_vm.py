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


def reconfigure_vm_disk_size(vm, disk_size_gb):
    try:
        # Değişiklikleri belirtmek için bir VimVMConfigSpec nesnesi oluşturun
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = []

        # Yeni disk ekleyin
        new_disk_spec = vim.vm.device.VirtualDeviceSpec()
        new_disk_spec.fileOperation = "create"
        new_disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

        # Yeni disk oluşturun
        new_disk_spec.device = vim.vm.device.VirtualDisk()
        # Yeni disk için kapasiteyi belirtin
        new_disk_spec.device.capacityInKB = disk_size_gb * 1024 * 1024
        # Yeni disk için disk modunu belirtin
        new_disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        new_disk_spec.device.backing.diskMode = 'persistent'
        # Yeni disk için disk türünü belirtin
        new_disk_spec.device.backing.thinProvisioned = True

        # Yeni birim numarasını alın
        new_disk_spec.device.unitNumber = get_available_unit_number(vm)

        # SCSI controller kullanmak için controller key değerini ayarlayın
        controllers = [d for d in vm.config.hardware.device if isinstance(d, vim.VirtualSCSIController)]
        if controllers:
            # Bir SCSI controller varsa, en ilk SCSI controller'ı kullanın
            new_disk_spec.device.controllerKey = controllers[0].key
        else:
            # Eğer bir SCSI controller yoksa, yeni bir SCSI controller ekleyin
            new_controller_spec = vim.vm.device.VirtualLsiLogicController()
            new_controller_spec.key = 1000
            new_controller_spec.busNumber = 0
            new_controller_spec.device = []

            controller_added_task = vm.ReconfigVM_Task(
                vim.vm.ConfigSpec(deviceChange=[vim.VirtualDeviceConfigSpec(device=new_controller_spec)]))
            WaitForTask(controller_added_task)

            # Yeni eklenen SCSI controller'ın anahtarını kullanın
            new_disk_spec.device.controllerKey = new_controller_spec.key

        spec.deviceChange.append(new_disk_spec)

        # Değişiklikleri uygulamak için ReconfigVM_Task'i çağırın
        task = vm.ReconfigVM_Task(spec=spec)
        WaitForTask(task)

        print("VM disk başarıyla yeniden yapılandırıldı.")

        # Her disk hakkında bilgiyi yazdırın
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                print(f"{device.deviceInfo.label} Disk: {device.capacityInKB / (1024 * 1024)} GB")

    except Exception as e:
        print(f"VM disk yeniden yapılandırma hatası: {e}")

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

    vm_name_to_reconfigure = "esxi_centos_sali"

    target_disk_size_gb = 8  # GB cinsinden istenen disk boyutu ile değiştirin

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # VM açık durumdaysa kapat
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM kapatılıyor...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    # Modify only the disk size
    reconfigure_vm_disk_size(vm_to_reconfigure, target_disk_size_gb)

    Disconnect(service_instance)


if __name__ == "__main__":
    main()
