from ESXi.IaaS.PowerOps import powerOn
from ESXi.IaaS.PowerOps import powerOff
from ESXi.IaaS.PowerOps import reboot_vm
from ESXi.IaaS.PowerOps import shut_down
from ESXi.IaaS.PowerOps import suspend_vm

def main():
    vm_name = "Deneme_sless"

    # esxi host bilgileri
    esxi_host_ip = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    #vm powerOn işlemi
    print("VM powerOn işlemi başlatıldı")
    powerOn.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    #vm powerOff işlemi
    print("VM powerOff işlemi başlatıldı")
    powerOff.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    #vm reboot işlemi
    print("VM reboot işlemi başlatıldı")
    reboot_vm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    #vm shut_down işlemi
    print("VM shut_down işlemi başlatıldı")
    shut_down.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    #vm suspend işlemi
    print("VM suspend işlemi başlatıldı")
    suspend_vm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)


if __name__ == "__main__":
    main()