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

def rename_files_in_folder(folder, content, datacenter, old_name, new_name):
    try:
        # FileManager'ı al
        file_manager = content.fileManager

        # Klasör içindeki dosyanın eski ve yeni yollarını belirle
        source_file_path = f"[{datacenter.name}] {folder}/{old_name}"
        target_file_path = f"[{datacenter.name}] {folder}/{new_name}"

        # Datacenter nesnesini al
        datacenter_obj = None
        for child in content.rootFolder.childEntity:
            if isinstance(child, vim.Datacenter):
                datacenter_obj = child
                break

        if datacenter_obj is None:
            print("Datacenter bulunamadı.")
            return

        # Dosyayı kopyala
        file_manager.CopyFile(sourceName=source_file_path, sourceDatacenter=datacenter_obj,
                              destinationName=target_file_path, destinationDatacenter=datacenter_obj)

        print(f"Dosya başarıyla kopyalandı: {target_file_path}")

        # Dosyayı sil
        file_manager.DeleteFile(sourceName=source_file_path, datacenter=datacenter_obj)

        print(f"Dosya başarıyla silindi: {source_file_path}")
    except Exception as e:
        print(f"Hata: {e}")

def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = connect.SmartConnect(host="10.14.45.11",
                              user="root",
                              pwd="Aa112233!",
                              sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    source_vm_name = "bkaan_deneme"

    source_vm = get_vm_by_name(content, source_vm_name)

    datastoreFile = {"nvram","vmdk","vmsd","vmxf","vmx","log"}

    if source_vm is not None:
        for i in datastoreFile:
            folder_name = "bkaan_deneme_clone"
            file_to_rename = "bkaan_deneme"+"."+i  # Specify the file to be renamed
            new_file_name = "new_bkaan_deneme"+"."+i  # Specify the new file name

            rename_files_in_folder(folder_name, content, source_vm.datastore[0], file_to_rename, new_file_name)
    else:
        print("VM bulunamadı.")

if __name__ == "__main__":
    main()
