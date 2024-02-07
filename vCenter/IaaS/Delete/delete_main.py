from ESXi.IaaS.Delete import destroyVm
from ESXi.IaaS.Delete import unRegister_Vm

def main():
    vm_name = "Deneme_sless"

    # esxi host bilgileri
    esxi_host_ip = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    select_mod = input("1- VM destroy\n2- VM unRegister\n")

    #vm destroy işlemi
    if select_mod == "1":
        print("VM destroy işlemi başlatıldı")
        destroyVm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    #vm unRegister işlemi
    if select_mod == "2":
        print("VM unRegister işlemi başlatıldı")
        unRegister_Vm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

if __name__ == "__main__":
    main()