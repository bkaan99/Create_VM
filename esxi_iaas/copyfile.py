import time
from pyVim import connect
from pyVmomi import vim
import os
from esxi_iaas.esxi_connection import *

def create_folder_in_datastore(content, datastore, source_folder_name, target_folder_name):
    try:
        # FileManager'ı al
        file_manager = content.fileManager

        # Kaynak ve hedef klasör yollarını belirle
        source_folder_path = f"[{datastore.name}] {source_folder_name}"
        target_folder_path = f"[{datastore.name}] {target_folder_name}"

        # Datacenter nesnesini al
        datacenter = None
        for child in content.rootFolder.childEntity:
            if isinstance(child, vim.Datacenter):
                datacenter = child
                break

        if datacenter is None:
            print("Datacenter bulunamadı.")
            return None

        # FileManager aracılığıyla klasörü oluştur
        task = file_manager.CopyFile(sourceName=source_folder_path, sourceDatacenter=datacenter,
                              destinationName=target_folder_path, destinationDatacenter=datacenter)

        WaitForTask(task)

        # Check if the task was successful
        if task.info.state == vim.TaskInfo.State.success:
            print(f"Klasör başarıyla kopyalandı: {target_folder_path}")

            # Oluşturulan klasörü al
            created_folder = target_folder_path

            if created_folder is not None:
                return created_folder
            else:
                print(f"Oluşturulan klasör alınamadı: {target_folder_path}")
                return None
        else:
            print(f"Klasör kopyalama işlemi başarısız. Task durumu: {task.info.state}")
            return None

    except Exception as e:
        print(f"Hata: {e}")
        return None

def WaitForTask(task):
    while task.info.state == vim.TaskInfo.State.running:
        task_info = task.info
        if hasattr(task_info, 'progress') and task_info.progress:
            print(f"Task Progress: {task_info.progress}%")

        time.sleep(3)

    return task.info.state

def print_files_in_folder(folder):
    try:
        # Klasördeki dosyaları al
        files = os.listdir(folder)
        print(f"Klasördeki dosyalar: {files}")
    except Exception as e:
        print(f"Hata: {e}")

def get_datastore_path_for_vm(vm):
    datastore_path = None
    if vm.config and vm.config.hardware and vm.config.hardware.device:
        for device in vm.config.hardware.device:
            if isinstance(device, vim.VirtualDisk):
                datastore_path = device.backing.fileName
                final_vm_folder_name = datastore_path.split("] ")[1].split("/")[0]
                break
    return final_vm_folder_name

def main(copied_vm_name, copied_folder_name, esxi_host_ip, esxi_user, esxi_password):

    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)

    # Klonlanacak VM'nin adını belirt
    source_vm_name = copied_vm_name

    # İsimle VM'yi bul
    source_vm = get_vm_by_name(content, source_vm_name)

    if source_vm is not None:

        if source_vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            print("VM açık olduğu için kopyalama işlemi için VM kapatılıyor...")
            task = source_vm.PowerOffVM_Task()
            WaitForTask(task)

        final_vm_folder_name = get_datastore_path_for_vm(source_vm)

        if final_vm_folder_name is not None:
            # Dizin adından datastore adını çıkar
            print(f"VM'nin datastore'daki klasör adı: {final_vm_folder_name}")
        else:
            print("VM'nin datastore klasör adını bulamadım.")

        # Klasörü oluştur
        folder_name = copied_folder_name
        folder = create_folder_in_datastore(content, source_vm.datastore[0], final_vm_folder_name, folder_name)

        if folder is not None:
            print(f"Klasör başarıyla oluşturuldu: {folder}")

            # Oluşturulan klasördeki dosyaları ekrana yazdır
            print_files_in_folder(folder)

        else:
            print("Klasör oluşturulurken bir hata oluştu.")
    else:
        print(f"Source VM '{source_vm_name}' not found.")

    # vCenter Server'dan bağlantıyı kapat
    connect.Disconnect(service_instance)

if __name__ == "__main__":
    main()
