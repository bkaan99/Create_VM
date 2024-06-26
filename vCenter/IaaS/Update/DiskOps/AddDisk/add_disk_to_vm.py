import time
from pyVim.connect import Disconnect
from vCenter.IaaS.Connections import vSphere_connection
from pyVmomi import vim

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


def reconfigure_vm_disk_size(vm, disk_size_gb, disk_mode):
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

        #FIXME: Buraya ilgili düzeltme tartışılacak. Default olarak persistent yapıldı şuanlık.
        new_disk_spec.device.backing.diskMode = 'persistent' # Default olarak ayarlandı.

        if disk_mode == 0:
            new_disk_spec.device.backing.diskMode = 'persistent'
        elif disk_mode == 1:
            new_disk_spec.device.backing.diskMode = 'independent_persistent'
        elif disk_mode == 2:
            new_disk_spec.device.backing.diskMode = 'independent_nonpersistent'

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

def main(vm_name_to_reconfigure, target_disk_size_gb, disk_mode, vCenter_host_ip, vCenter_user, vCenter_password):

    service_instance, content = vSphere_connection.create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_to_reconfigure = vSphere_connection.get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # VM açık durumdaysa shutdown yap
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print(f"{vm_to_reconfigure.name} powered on olduğu için kapatılıyor...")
        task = vm_to_reconfigure.ShutdownGuest()
        while vm_to_reconfigure.runtime.powerState != vim.VirtualMachinePowerState.poweredOff:
            print("VM Power Off olması bekleniyor...")
            time.sleep(3)  # Her saniye güç durumunu kontrol edelim

    # Modify only the disk size
    reconfigure_vm_disk_size(vm_to_reconfigure, disk_size_gb=target_disk_size_gb, disk_mode=disk_mode)

    print("VM açılıyor...")
    if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        task = vm_to_reconfigure.PowerOnVM_Task()
        WaitForTask(task)

    time.sleep(5)

    Disconnect(service_instance)