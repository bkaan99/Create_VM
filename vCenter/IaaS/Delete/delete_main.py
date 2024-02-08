import base64
import sys

from ESXi.IaaS.Delete import destroyVm
from ESXi.IaaS.Delete import unRegister_Vm
from vCenter.IaaS.Connections.db_connection import *
from vCenter.IaaS.Create.CloneControlPlane import get_id_list

def get_id_list():
    global flowUUID
    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")
    li = list(mystring.replace(' ', '').split(","))

    #TODO: flowUUID tekrar eklenecek. Yorumda olan yerler açılacak.
    if len(li) > 0:
        #flowUUID = li[0];
        #li.pop(0)
        print(f"Removed value: {li}")
    else:
        print("List is empty.")

    return li #, flowUUID

def main():

    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    # TODO: flowUUID tekrar eklenecek.
    vmIdList = get_id_list()

    for vmid in vmIdList:

        print(f"VM ID: {vmid}")
        # get vm config
        vm_config_lists = get_vmList_Config(vmid)

        vm_config_lists_vm_name = vm_config_lists[1]

        clone_name = vm_config_lists_vm_name

        #vm destroy işlemi
        print("VM destroy işlemi başlatıldı")
        destroyVm.main(clone_name, vCenter_host_ip, vCenter_user, vCenter_password)


    # select_mod = input("1- VM destroy\n2- VM unRegister\n")

    # #vm destroy işlemi
    # if select_mod == "1":
    #     print("VM destroy işlemi başlatıldı")
    #     destroyVm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)
    #
    # #vm unRegister işlemi
    # if select_mod == "2":
    #     print("VM unRegister işlemi başlatıldı")
    #     unRegister_Vm.main(vm_name, esxi_host_ip, esxi_user, esxi_password)

if __name__ == "__main__":
    main()