from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def reconfigure_vm(vm, cpu_count, memory_mb, disk_size_gb):
    try:
        # Değişiklikleri belirtmek için bir VimVMConfigSpec nesnesi oluşturun
        spec = vim.vm.ConfigSpec()
        spec.numCPUs = cpu_count
        spec.memoryMB = memory_mb
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

        # Eğer bir birim numarası varsa, en son birim numarasının bir fazlasını kullanın
        if hasattr(vm.config, 'hardware') and hasattr(vm.config.hardware, 'device'):
            existing_disks = [d for d in vm.config.hardware.device if isinstance(d, vim.VirtualDisk)]
            if existing_disks:
                # Bir birim numarası varsa, en son birim numarasının bir fazlasını kullanın
                new_disk_spec.device.unitNumber = max([disk.unitNumber for disk in existing_disks]) + 1
            else:
                # Eğer bir birim numarası yoksa, 0'ı kullanın
                new_disk_spec.device.unitNumber = 0

        # Eğer bir kontrol cihazı varsa, onu kullanın
        controllers = [d for d in vm.config.hardware.device if isinstance(d, vim.VirtualController)]
        if controllers:
            # Bir kontrol cihazı varsa, en ilk kontrol cihazını kullanın
            new_disk_spec.device.controllerKey = controllers[0].key
        else:
            # Eğer bir kontrol cihazı yoksa, yeni bir kontrol cihazı ekleyin
            new_controller_spec = vim.vm.device.VirtualController()
            new_controller_spec.key = 1000
            new_controller_spec.busNumber = 0
            new_controller_spec.device = []

            controller_added_task = vm.ReconfigVM_Task(
                vim.vm.ConfigSpec(deviceChange=[vim.VirtualDeviceConfigSpec(device=new_controller_spec)]))
            WaitForTask(controller_added_task)

            # Yeni eklenen kontrol cihazının anahtarını kullanın
            new_disk_spec.device.controllerKey = new_controller_spec.key

        spec.deviceChange.append(new_disk_spec)

        # Değişiklikleri uygulamak için ReconfigVM_Task'i çağırın
        task = vm.ReconfigVM_Task(spec=spec)
        WaitForTask(task)

        print("VM başarıyla yeniden yapılandırıldı.")
        print("VM yeni Bellek: %s" % memory_mb)
        print("VM yeni CPU: %s" % cpu_count)

        # Her disk hakkında bilgiyi yazdırın
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                print(f"{device.deviceInfo.label} Disk: {device.capacityInKB / (1024 * 1024)} GB")

    except Exception as e:
        print(f"VM yeniden yapılandırma hatası: {e}")

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

    target_cpu_count = 2  # İstenen CPU sayısı ile değiştirin
    target_memory_mb = 4096  # MB cinsinden istenen bellek boyutu ile değiştirin
    target_disk_size_gb = 48  # GB cinsinden istenen disk boyutu ile değiştirin

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # VM açık durumdaysa kapat
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print("VM kapatılıyor...")
        task = vm_to_reconfigure.PowerOffVM_Task()
        WaitForTask(task)

    reconfigure_vm(vm_to_reconfigure, target_cpu_count, target_memory_mb, target_disk_size_gb)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
