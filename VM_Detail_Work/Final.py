from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# ESXi host bilgileri
esxi_host = "10.14.45.11"
username = "root"
password = "Aa112233!"

# Bağlantı yap
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_NONE  # Sertifika doğrulamasını devre dışı bırak

si = SmartConnect(host=esxi_host, user=username, pwd=password, port=443, sslContext=context)

# Sanal makineleri al
content = si.RetrieveContent()
container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vms = container.view

# Sanal makineleri listeleyerek tüm detayları ekrana yazdır
print("Sanal Makineler:")
for vm in vms:
    print(f"VM Adı: {vm.summary.config.name}")
    print(f"VM ID: {vm.summary.vm}")
    print(f"CPU Sayısı: {vm.summary.config.numCpu}")
    print(f"RAM Miktarı: {vm.summary.config.memorySizeMB} MB")
    print(f"İşletim Sistemi: {vm.summary.config.guestFullName}")
    print(f"Sanal Diskler:")

    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualDisk):
            print(f"  Disk Adı: {device.deviceInfo.label}")
            print(f"  Kapasite: {device.capacityInKB / 1024 / 1024} GB")
            print(f"  Disk Tipi: {device.backing.diskMode}")
            print()

    print("-" * 30)

# Bağlantıyı kapat
Disconnect(si)
