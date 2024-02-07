import base64
import sys
from ESXi.IaaS.Create import registry_vm
from ESXi.IaaS.Create import copyfile
from ESXi.IaaS.Create import reconfig_vm
from ESXi.IaaS.db_connection import *

# def db_logger():
#     t = connect_Postgres()
#     cursor = t.cursor()
#     flowUUID = 1
#     workflowInfoTable = pd.read_sql_query("select * from kr_workflow_info where uuid=" + str(flowUUID), t)
#
#     #bir tablo içerisinde ki alanlarrın içerisini dolduruyoruz.

def get_id_list():
    global flowUUID
    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")
    li = list(mystring.replace(' ', '').split(","))

    if len(li) > 0:
        flowUUID = li[0];
        li.pop(0)
        print(f"Removed value: {li}")
    else:
        print("List is empty.")

    return li, flowUUID

def check_vm_os_family(os_family, os_version):

    if os_family == "Windows":
        if os_version == "Windows Server 2016":
            template_name = "Windows-Server-2016"
            print("Windows işletim sistemi için VM oluşturuluyor")
            return template_name

        if os_version == "Windows 2018":
            template_name = "bkaan_deneme"
            print("Windows işletim sistemi için VM oluşturuluyor")
            return template_name

    elif os_family == "Linux":
        if os_version == "SUSE Linux":
            template_name = "SUSE-Temp-15-3"
            print("Linux işletim sistemi için VM oluşturuluyor")
            return template_name

        if os_version == "Ubuntu":
            template_name = "Ubuntu-Temp-20-04"
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
    #
    # #önceden kurulmuş vm 'i kopyalayacağımız için vm adını belirtiyoruz.
    # copying_vm_name = "SUSE-Temp-15-3"
    #
    # #burada ise cloen olacak vm icin datastore icerisinde bir klasör adı belirtiyoruz.
    #
    # #burada ise kayıt edilme ile oluşacak olan vm adını belirtiyoruz.
    # RegisterVm_name = "Clone-SUSE-Temp-15-3"
    #
    # copied_folder_name = RegisterVm_name


    #esxi host bilgileri
    esxi_host_ip = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    #cpu ve ram değerleri
    # cpu_count = 6
    # memory_mb = 4096
    # disk_size_gb = 48

    vmIdList, flowUUID = get_id_list()

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

        copying_vm_name = check_vm_os_family(vm_config_lists_os_family, vm_config_lists_os_version)
        RegisterVm_name = vm_config_lists_vm_name
        copied_folder_name = RegisterVm_name

        cpu_count = int(vm_config_lists_cpu)
        memory_mb = int(vm_config_lists_ram_size) * 1024
        disk_size_gb = int(vm_disk_size_gb)

        #Dosya kopyalama işlemi
        print("VM Dosya kopyalama işlemi başlatıldı")
        copyfile.main(copying_vm_name, copied_folder_name, esxi_host_ip, esxi_user, esxi_password)

        #Vm kayıt işlemi
        print("VM kayıt işlemi başlatıldı")
        registry_vm.main(RegisterVm_name, copying_vm_name, esxi_host_ip, esxi_user, esxi_password, copied_folder_name)

        #Vm reconfig işlemi
        print("VM reconfig işlemi başlatıldı")
        reconfig_vm.main(RegisterVm_name, esxi_host_ip, esxi_user, esxi_password, cpu_count, memory_mb, disk_size_gb)

        print("IAAS Create işlemi tamamlandı")
if __name__ == "__main__":
    main()
