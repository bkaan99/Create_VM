from ESXi.IaaS.Create import registry_vm
from ESXi.IaaS.Create import copyfile
from ESXi.IaaS.Create import reconfig_vm
import time


def main():
    print("IAAS Create işlemi başlatıldı")

    #önceden kurulmuş vm 'i kopyalayacağımız için vm adını belirtiyoruz.
    copying_vm_name = "Ubuntu_Deneme"

    #burada ise cloen olacak vm icin datastore icerisinde bir klasör adı belirtiyoruz.

    #burada ise kayıt edilme ile oluşacak olan vm adını belirtiyoruz.
    RegisterVm_name = "Pzt_Ubuntu_Deneme"

    copied_folder_name = RegisterVm_name


    #esxi host bilgileri
    esxi_host_ip = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    #cpu ve ram değerleri
    cpu_count = 6
    memory_mb = 4096
    disk_size_gb = 48

    #Dosya kopyalama işlemi
    print("VM Dosya kopyalama işlemi başlatıldı")
    copyfile.main(copying_vm_name, copied_folder_name, esxi_host_ip, esxi_user, esxi_password)

    #Vm kayıt işlemi
    print("VM kayıt işlemi başlatıldı")
    registry_vm.main(RegisterVm_name, copying_vm_name, esxi_host_ip, esxi_user, esxi_password, copied_folder_name)

    #Vm reconfig işlemi
    print("VM reconfig işlemi başlatıldı")
    reconfig_vm.main(RegisterVm_name, esxi_host_ip, esxi_user, esxi_password, cpu_count, memory_mb, disk_size_gb)

    print("IAAS Create işlemi tamamlandı")
if __name__ == "__main__":
    main()
