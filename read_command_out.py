import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import requests


def download_file_from_vm(vm, content, auth, guest_file_path):
    file_manager = content.guestOperationsManager.fileManager

    # Dosyanın indirme işlemini başlat
    transfer_info = file_manager.InitiateFileTransferFromGuest(vm, auth, guest_file_path)
    url = transfer_info.url

    # URL'den dosya içeriğini al
    response = requests.get(url, verify=False)

    # Dosya içeriğini bir değişkene ata
    file_content = response.content

    return file_content


def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def main():
    # ESXi bilgileri
    esxi_host = "10.14.45.10"
    esxi_user = "administrator@vsphere.local"
    esxi_password = "Aa112233!"

    # VM bilgileri
    vm_name = "bkaan_sapaas"  # Sanal makinenin adı
    vm_username = "root"
    vm_password = "111111"

    # Dosyanın bulunduğu konum sanal makinede
    guest_file_path = "/tmp/output.txt"

    # ESXi'ye bağlan
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host=esxi_host, user=esxi_user, pwd=esxi_password, sslContext=ssl_context)
    content = service_instance.RetrieveContent()

    # Belirtilen isme sahip sanal makineyi bul
    target_vm = get_vm_by_name(content, vm_name)

    if target_vm is None:
        print(f"VM with name {vm_name} not found.")
        Disconnect(service_instance)
        return

    try:
        auth = vim.vm.guest.NamePasswordAuthentication(username=vm_username, password=vm_password)

        # Dosyayı indir ve içeriğini bir değişkene ata
        file_content = download_file_from_vm(target_vm, content, auth, guest_file_path)

        # Dosya içeriğini ekrana yazdır
        print("File content:")
        print(file_content.decode("utf-8"))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        Disconnect(service_instance)


if __name__ == "__main__":
    main()
