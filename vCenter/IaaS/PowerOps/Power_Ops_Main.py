import sys
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

    select_power_mod = input("1- Power On\n2- Power Off\n3- Reboot\n4- Shut Down\n5- Suspend\n")
    if select_power_mod == "1":
        print("VM powerOn işlemi başlatıldı")
        powerOn.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    if select_power_mod == "2":
        print("VM powerOff işlemi başlatıldı")
        powerOff.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    if select_power_mod == "3":
        print("VM reboot işlemi başlatıldı")
        reboot_vm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    if select_power_mod == "4":
        print("VM shut_down işlemi başlatıldı")
        shut_down.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    if select_power_mod == "5":
        print("VM suspend işlemi başlatıldı")
        suspend_vm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

    else:
        print("Yanlış seçim yaptınız.")
        sys.exit()

if __name__ == "__main__":
    main()