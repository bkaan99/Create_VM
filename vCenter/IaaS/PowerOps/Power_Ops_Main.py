# import sys
# sys.path.append('/home/gardiyan/Gardiyan/Server/pfms/apache-karaf-5005/GH-Plugins')

import sys
from vCenter.IaaS.Connections.db_connection import *
from vCenter.IaaS.PowerOps import powerOff
from vCenter.IaaS.PowerOps import powerOn
from vCenter.IaaS.PowerOps import reboot_vm
from vCenter.IaaS.PowerOps import shut_down
from vCenter.IaaS.PowerOps import suspend_vm
from vCenter.IaaS.ExternelFiles import get_id_list_controller


def main():
    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    vmIdList = get_id_list_controller.get_id_list()

    PowerOpsCode = get_id_list_controller.get_powerOpsCode_from_id()

    for vmid in vmIdList:
        print(f"VM ID: {vmid}")

        # get vm config
        vm_config_lists = get_vmList_Config(vmid)
        vm_config_lists_VmName = vm_config_lists[3]
        vm_name = vm_config_lists_VmName

        print(f"VM Name: {vm_name}")

        if PowerOpsCode == 1:
            print("VM powerOn işlemi başlatıldı")
            powerOn.main(vm_name=vm_name,
                         vCenter_host_ip=vCenter_host_ip,
                         vCenter_user=vCenter_user,
                         vCenter_password=vCenter_password)

        if PowerOpsCode == 2:
            print("VM powerOff işlemi başlatıldı")
            powerOff.main(vm_name=vm_name,
                          vCenter_host_ip=vCenter_host_ip,
                          vCenter_user=vCenter_user,
                          vCenter_password=vCenter_password)

        if PowerOpsCode == 3:
            print("VM reboot işlemi başlatıldı")
            reboot_vm.main(vm_name=vm_name,
                           vCenter_host_ip=vCenter_host_ip,
                           vCenter_user=vCenter_user,
                           vCenter_password=vCenter_password)

        if PowerOpsCode == 4:
            print("VM shut_down işlemi başlatıldı")
            shut_down.main(vm_name=vm_name,
                           vCenter_host_ip=vCenter_host_ip,
                           vCenter_user=vCenter_user,
                           vCenter_password=vCenter_password)

        if PowerOpsCode == 5:
            print("VM suspend işlemi başlatıldı")
            suspend_vm.main(vm_name=vm_name,
                            vCenter_host_ip=vCenter_host_ip,
                            vCenter_user=vCenter_user,
                            vCenter_password=vCenter_password)

        else:
            print("Yanlış seçim yaptınız.")
            sys.exit()

if __name__ == "__main__":
    main()