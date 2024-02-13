import base64
import sys
import re
from vCenter.IaaS.PowerOps import powerOn
from vCenter.IaaS.PowerOps import powerOff
from vCenter.IaaS.PowerOps import reboot_vm
from vCenter.IaaS.PowerOps import shut_down
from vCenter.IaaS.PowerOps import suspend_vm
from vCenter.IaaS.Connections.db_connection import *


def get_id_list():
    global flowUUID
    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")
    li = list(mystring.replace(' ', '').split(","))

    powerOpsCode = base64.b64decode(sys.argv[2]).decode('UTF-8')
    match = re.match(r"\[([^:]+):(\d+)\]", powerOpsCode)

    if match:
        powerOpsCode_key = match.group(1)
        powerOpsCode_value = int(match.group(2))  # Eğer sayı olarak almak istiyorsanız int dönüşümü yapabilirsiniz
        print(f"Key: {powerOpsCode_key}, Value: {powerOpsCode_value}")
    else:
        print("Gelen değer istenen formatta değil.")


    #TODO: flowUUID tekrar eklenecek. Yorumda olan yerler açılacak.
    if len(li) > 0:
        #flowUUID = li[0];
        #li.pop(0)
        print(f"Removed value: {li}")
    else:
        print("List is empty.")

    return li , powerOpsCode_value#, flowUUID

def main():

    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    # TODO: flowUUID tekrar eklenecek.
    id_list = get_id_list()
    vmIdList = id_list[0]
    PowerOpsCode  = id_list[1]

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