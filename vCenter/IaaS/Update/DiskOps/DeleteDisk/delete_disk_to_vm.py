from pyVim.connect import Disconnect
from vCenter.IaaS.Connections import vSphere_connection
from pyVmomi import vim

def delete_disk_file_from_datastore(datastore, datastore_path):
    try:
        browser = datastore.browser
        browser.DeleteFile(datastore_path)
        print(f"{datastore_path} dosyası başarıyla datastore'dan silindi.")
    except Exception as delete_error:
        print(f"Datastore'dan dosya silme hatası: {delete_error}")

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

        print(f"{disk_name} adına sahip disk başarıyla kaldırıldı. Disk boyutu: {disk_to_remove.capacityInKB / (1024 * 1024)} GB")

        # Disk dosyasını datastore'dan da sil
        datastore_path = disk_to_remove.backing.fileName
        datastore = disk_to_remove.backing.datastore
        if datastore_path and datastore:
            delete_disk_file_from_datastore(datastore, datastore_path)
    except Exception as e:
        print(f"Disk kaldırma hatası: {e}")

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

def get_vm_disk_info(vm):
    disk_info = []

    for device in vm.config.hardware.device:
        if isinstance(device, vim.VirtualDisk):
            disk_name = device.deviceInfo.label
            disk_size_gb = device.capacityInKB / (1024 * 1024)  # Byte cinsinden kapasiteyi GB'ye çevir
            disk_info.append({"Disk Name": disk_name, "Disk Size (GB)": disk_size_gb})

    return disk_info

def main(vm_name_to_reconfigure, vCenter_host_ip, vCenter_user, vCenter_password, hard_disk_name_to_delete: str):

    service_instance, content = vSphere_connection.create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_to_reconfigure = vSphere_connection.get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    # Silinecek disk adı
    vm_disk_info = get_vm_disk_info(vm_to_reconfigure)
    for disk in vm_disk_info:
        print(f"Disk Name: {disk['Disk Name']}, Disk Size (GB): {disk['Disk Size (GB)']}")
        #disk adı yada boyutu doğru girilirse silme işlemi yapılır.
        if disk['Disk Name'] == hard_disk_name_to_delete:
            delete_disk_by_name(vm_to_reconfigure, disk['Disk Name'])

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
