import base64
import sys
from ESXi.IaaS.Delete import destroyVm
from vCenter.IaaS.Connections.db_connection import *


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


if __name__ == "__main__":
    main()