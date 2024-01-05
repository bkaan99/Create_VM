from esxi_iaas import copyfile
from esxi_iaas import registry_vm

def main():
    print("Vm Oluşturma İşlemi Başladı")
    copied_vm_name = "bkaan_centos"
    copied_folder_name = "kardes"


    RegisterVm_name = "esxi_centos_cuma_mesai"


    #Dosya kopyalama işlemi
    #copyfile.main(copied_vm_name, copied_folder_name)

    #Vm kayıt işlemi
    registry_vm.main(RegisterVm_name)



if __name__ == "__main__":
    main()
