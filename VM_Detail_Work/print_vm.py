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


# Datacenter bilgisini al
datacenters = content.rootFolder.childEntity
print("Datacenter Bilgisi:")
for datacenter in datacenters:
    print("Datacenter Name:", datacenter.name)
    print("Datacenter VM Folder:", datacenter.vmFolder.name)


# Sanal makineleri listeleyerek tüm detayları ekrana yazdır
print("Sanal Makineler:")

for vm in vms:
   print(vm.name)

# Bağlantıyı kapat
Disconnect(si)
