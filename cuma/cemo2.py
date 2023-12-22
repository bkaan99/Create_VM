from pyVim import connect
from pyVmomi import vim
import ssl
import os
import shutil


## çalışan py
def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def create_folder_in_datastore(content, datastore, folder_name):
    try:
        # FileManager'ı al
        file_manager = content.fileManager

        # Oluşturulacak klasörün yolunu belirle
        folder_path = f"[{datastore.name}] {folder_name}"

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
        file_manager.MakeDirectory(name=folder_path, datacenter=datacenter)

        print(f"Klasör oluşturuldu: {folder_path}")

        # Oluşturulan klasörü al
        created_folder = folder_path

        if created_folder is not None:
            return created_folder
        else:
            print(f"Oluşturulan klasör alınamadı: {folder_path}")
            return None

    except Exception as e:
        print(f"Hata: {e}")
        return None

def copy_files_to_folder(source_folder, target_folder):
    try:
        # Kaynak dizini kontrol et
        if not os.path.exists(source_folder):
            print(f"Kaynak dizin bulunamadı: {source_folder}")
            return

        # Hedef dizini kontrol et ve oluştur
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Kaynak dizinindeki dosyaları hedef dizine kopyala
        for filename in os.listdir(source_folder):
            source_file_path = os.path.join(source_folder, filename)
            target_file_path = os.path.join(target_folder, filename)

            # Dosyayı kopyala
            shutil.copy2(source_file_path, target_file_path)
            print(f"{filename} dosyası başarıyla kopyalandı.")

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
        folder_name = "bkaan_deneme_clone"
        folder = create_folder_in_datastore(content, source_vm.datastore[0], folder_name)

        if folder is not None:
            # Dosyaları kopyala
            source_folder_path = source_vm.config.files.vmPathName.replace("[", "").replace("]", "")
            source_folder = os.path.join(source_folder_path, "")
            copy_files_to_folder(source_folder, folder)
            print(f"Dosyalar başarıyla kopyalandı.")

        else:
            print("Klasör oluşturulurken bir hata oluştu.")
    else:
        print(f"Source VM '{source_vm_name}' not found.")

    # vCenter Server'dan bağlantıyı kapat
    connect.Disconnect(si)

if __name__ == "__main__":
    main()
