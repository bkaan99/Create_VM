import time

from pyVim import connect
from pyVmomi import vim
import ssl
import os


def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

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

        time.sleep(2)

    return task.info.state

def print_files_in_folder(folder):
    try:
        # Klasördeki dosyaları al
        files = os.listdir(folder)
        print(f"Klasördeki dosyalar: {files}")
    except Exception as e:
        print(f"Hata: {e}")

def main():
    # SSL sertifikası doğrulamasını devre dışı bırak (self-signed sertifikalar için)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # vCenter Server'a bağlan
    si = connect.SmartConnect(host="10.14.45.11",
                              user="root",
                              pwd="Aa112233!",
                              sslContext=ssl_context)

    # İçerik objesini al
    content = si.RetrieveContent()

    # Klonlanacak VM'nin adını belirt
    source_vm_name = "bkaan_deneme"

    # İsimle VM'yi bul
    source_vm = get_vm_by_name(content, source_vm_name)

    if source_vm is not None:
        # Klasörü oluştur
        folder_name = "gurgen33"
        folder = create_folder_in_datastore(content, source_vm.datastore[0], source_vm_name, folder_name)

        if folder is not None:
            print(f"Klasör başarıyla oluşturuldu: {folder}")

            # Oluşturulan klasördeki dosyaları ekrana yazdır
            print_files_in_folder(folder)

        else:
            print("Klasör oluşturulurken bir hata oluştu.")
    else:
        print(f"Source VM '{source_vm_name}' not found.")

    # vCenter Server'dan bağlantıyı kapat
    connect.Disconnect(si)

if __name__ == "__main__":
    main()
