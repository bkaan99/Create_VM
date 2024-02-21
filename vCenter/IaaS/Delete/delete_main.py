# import sys
# sys.path.append('/home/gardiyan/Gardiyan/Server/pfms/apache-karaf-5005/GH-Plugins')

import base64
import sys
from ESXi.IaaS.Delete import destroyVm
from vCenter.IaaS.Connections.db_connection import *
from vCenter.IaaS.ExternelFiles import get_id_list_controller

def main():

    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    vmIdList = get_id_list_controller.get_id_list()

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