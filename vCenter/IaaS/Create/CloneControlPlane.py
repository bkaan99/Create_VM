import base64
import sys
import time
from vCenter.IaaS.Connections.db_connection import *
from vCenter.IaaS.Create import clone_from_template, reconfig_vm
from vCenter.IaaS.PowerOps import powerOn

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

def check_vm_os_family(os_family, os_version):

    if os_family == "Windows":
        if os_version == "Windows Server 2016":
            template_name = "bkaan_windows_template"
            print("Windows işletim sistemi için VM oluşturuluyor")
            return template_name

        if os_version == "Windows 2018":
            template_name = "bkaan_windows_template"
            print("Windows işletim sistemi için VM oluşturuluyor")
            return template_name

        else:
            template_name = "bkaan_windows_template"
            return template_name

    elif os_family == "Linux":
        if os_version == "SUSE Linux":
            template_name = "SUSE-Temp-15-3"
            print("Linux işletim sistemi için VM oluşturuluyor")
            return template_name

        if os_version == "Ubuntu":
            template_name = "Ubuntu_Deneme"
            print("Linux işletim sistemi için VM oluşturuluyor")
            return template_name

    elif os_family == "Other":
        pass

    elif os_family == "MacOS":
        pass

    else:
        print("OS family not found")

def main():
    print("IAAS Create işlemi başlatıldı")

    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    #TODO: flowUUID tekrar eklenecek.
    vmIdList = get_id_list()

    for vmid in vmIdList:
        print(f"VM ID: {vmid}")
        #get vm config
        vm_config_lists = get_vmList_Config(vmid)

        vm_config_lists_os_family = vm_config_lists[0]
        vm_config_lists_vm_name = vm_config_lists[1]
        vm_config_lists_cpu = vm_config_lists[2]
        vm_config_lists_ram_size = vm_config_lists[3]
        vm_config_lists_os_version = vm_config_lists[4]

        #get first disk config
        vm_disk_size_gb = get_first_disik_Config(vmid)

        template_name = check_vm_os_family(vm_config_lists_os_family, vm_config_lists_os_version)
        clone_name = vm_config_lists_vm_name
        copied_folder_name = clone_name

        cpu_count = int(vm_config_lists_cpu)
        memory_mb = int(vm_config_lists_ram_size) * 1024
        disk_size_gb = int(vm_disk_size_gb)

        # Clone VM from template
        clone_from_template.main(vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password, template_name=template_name, clone_name=clone_name)

        time.sleep(3)
        # Reconfigure VM
        reconfig_vm.main(vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password, clone_name=clone_name, cpu_count=cpu_count, memory_mb=memory_mb, disk_size_gb=disk_size_gb)

        # Power on VM

        print("IAAS Create işlemi tamamlandı")
if __name__ == "__main__":
    main()
