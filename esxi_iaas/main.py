from esxi_iaas import copyfile
from esxi_iaas import registry_vm

def main():
    print("IAAS Create işlemi başlatıldı")

    #önceden kurulmuş vm 'i kopyalayacağımız için vm adını belirtiyoruz.
    copied_vm_name = "referans_centos"

    #burada ise cloen olacak vm icin datastore icerisinde bir klasör adı belirtiyoruz.
    copied_folder_name = "kardes"

    #burada ise kayıt edilme ile oluşacak olan vm adını belirtiyoruz.
    RegisterVm_name = "esxi_centos_cumartesi"


    #esxi host bilgileri
    esxi_host_ip = "100.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"


    #Dosya kopyalama işlemi
    copyfile.main(copied_vm_name, copied_folder_name, esxi_host_ip, esxi_user, esxi_password)

    #Vm kayıt işlemi
    #registry_vm.main(RegisterVm_name , copied_vm_name, esxi_host_ip, esxi_user, esxi_password)



if __name__ == "__main__":
    main()
