import base64
import string
import sys
import time
from vCenter.IaaS.Connections.db_connection import *
from vCenter.IaaS.Create import vmtoolsstatus, clone_from_template
from vCenter.IaaS.Update.DiskOps.AddDisk import add_disk_to_vm
from vCenter.IaaS.Update.DiskOps.SetDisk import execute_disk_to_windows, execute_disk_to_linux, execute_sapaas_disk_to_centos
from vCenter.IaaS.Update.NetworkOps.AddNetworkAdapter import add_network_adapter
from vCenter.IaaS.Update.NetworkOps.CheckNetworkAdapter import check_network_adapter_existence
from vCenter.IaaS.Update.NetworkOps.SetIPAdress import execute_ipAddress_windows, execute_ipAddress_to_linux


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

    if "Windows" in os_family:
        if "Windows Server 2016" in os_version:
            template_name = "bkaan_windows_template"
            print("Windows işletim sistemi için VM oluşturuluyor")
            return template_name

        if "Windows 2018" in os_version:
            template_name = "bkaan_windows_template"
            print("Windows işletim sistemi için VM oluşturuluyor")
            return template_name

        else:
            template_name = "bkaan_windows_template"
            return template_name

    elif "Linux" in os_family:
        if "SUSE" in os_version:
            template_name = "SUSE-Temp-15-3"
            print("Linux işletim sistemi için VM oluşturuluyor")
            return template_name

        if "Ubuntu" in os_version:
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

        vm_config_lists_id = vm_config_lists[0]
        vm_config_lists_Cpu = int(vm_config_lists[1])
        vm_config_lists_RamSize = int(vm_config_lists[2]) * 1024
        vm_config_lists_VmName = vm_config_lists[3]
        vm_config_lists_HostName = vm_config_lists[4]
        vm_config_lists_IpAdress = vm_config_lists[5]
        vm_config_lists_Environment = vm_config_lists[6]
        vm_config_lists_OperatingSystemInformation = vm_config_lists[7]
        vm_config_lists_OperatingSystemVersion = vm_config_lists[8]
        vm_config_lists_InternetConnection = vm_config_lists[9]
        vm_config_lists_VirtualizationTechnology = vm_config_lists[10]
        vm_config_lists_PFMSConfigurationId = vm_config_lists[11]

        #get pfms config type
        pfms_config_type = vm_config_lists[12]


        #get first disk config
        vm_disk_list = get_first_disik_Config(vmid)

        vm_disk_size_gb = int(vm_disk_list[0])

        vm_disk_list.pop(0)

        other_disk_list = vm_disk_list

        template_name = check_vm_os_family(vm_config_lists_OperatingSystemInformation, vm_config_lists_OperatingSystemVersion)
        clone_name = vm_config_lists_VmName
        copied_folder_name = clone_name


        ### Clone VM from template
        clone_from_template.main(vCenter_host_ip=vCenter_host_ip,
                                 vCenter_user=vCenter_user,
                                 vCenter_password=vCenter_password,
                                 template_name=template_name,
                                 clone_name=clone_name,
                                 disk_size_gb=vm_disk_size_gb,
                                 memory_mb=vm_config_lists_RamSize,
                                 cpu_count=vm_config_lists_Cpu)

        while vmtoolsstatus.main(vCenterIP=vCenter_host_ip, username=vCenter_user,
                                 password=vCenter_password,
                                 vm_name=clone_name) == False:
            print("VM Tools status kontrol ediliyor")
            time.sleep(3)

        # check internet connection
        if vm_config_lists_InternetConnection == True:
            network_adapter_existence_value, device_label = check_network_adapter_existence.main(vCenter_host_ip=vCenter_host_ip,
                                                                                                 vCenter_user=vCenter_user,
                                                                                                 vCenter_password=vCenter_password,
                                                                                                 vm_name=clone_name)

            if network_adapter_existence_value:
                vm_tools_status = vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                                     username=vCenter_user,
                                                     password=vCenter_password,
                                                     vm_name=clone_name)

                if vm_tools_status:
                    if vm_config_lists_OperatingSystemInformation == "Windows":
                        execute_ipAddress_windows.main(vm_name=clone_name,
                                                       vCenter_host_ip=vCenter_host_ip,
                                                       vCenter_user=vCenter_user,
                                                       vCenter_password=vCenter_password,
                                                       ipAddress=vm_config_lists_IpAdress)
                    elif vm_config_lists_OperatingSystemInformation == "Linux":
                        execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                        vCenter_host_ip=vCenter_host_ip,
                                                        vCenter_user=vCenter_user,
                                                        vCenter_password=vCenter_password,
                                                        ipAddress=vm_config_lists_IpAdress)

                else:
                    time.sleep(5)
                    retry_count = 0
                    max_retries = 3
                    while retry_count < max_retries:
                        time.sleep(10)
                        vm_tools_status = vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                                             username=vCenter_user,
                                                             password=vCenter_password,
                                                             vm_name=clone_name)
                        if vm_tools_status:
                            if vm_config_lists_OperatingSystemInformation == "Windows":
                                execute_ipAddress_windows.main(vm_name=clone_name,
                                                               vCenter_host_ip=vCenter_host_ip,
                                                               vCenter_user=vCenter_user,
                                                               vCenter_password=vCenter_password,
                                                               ipAddress=vm_config_lists_IpAdress)

                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                                vCenter_host_ip=vCenter_host_ip,
                                                                vCenter_user=vCenter_user,
                                                                vCenter_password=vCenter_password,
                                                                ipAddress=vm_config_lists_IpAdress)
                            break
                        retry_count += 1

                if not vm_tools_status:
                    raise Exception("VM Tools status could not be verified after retrying.")

            elif network_adapter_existence_value == False:
                add_network_adapter.main(vm_name_to_reconfigure=clone_name,
                                         vCenter_host_ip=vCenter_host_ip,
                                         vCenter_user=vCenter_user,
                                         vCenter_password=vCenter_password)

                if vm_config_lists_OperatingSystemInformation == "Windows":
                    execute_ipAddress_windows.main(vm_name=clone_name,
                                                   vCenter_host_ip=vCenter_host_ip,
                                                   vCenter_user=vCenter_user,
                                                   vCenter_password=vCenter_password,
                                                   ipAddress=vm_config_lists_IpAdress)

                elif vm_config_lists_OperatingSystemInformation == "Linux":
                    execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                    vCenter_host_ip=vCenter_host_ip,
                                                    vCenter_user=vCenter_user,
                                                    vCenter_password=vCenter_password,
                                                    ipAddress=vm_config_lists_IpAdress)

        # add disk to VM
        if len(other_disk_list) > 0:
            allowed_letters = string.ascii_uppercase[4:]  # "E" harfinden başlayarak "Z" harfine kadar olan harfler
            current_letter = allowed_letters[0]
            counter = 0
            disk_mount_location = "hana/shared"
            for disk_size_gb in other_disk_list:

                add_disk_to_vm.main(vm_name_to_reconfigure=clone_name,
                                    target_disk_size_gb=disk_size_gb,
                                    esxi_host_ip=vCenter_host_ip,
                                    esxi_user=vCenter_user,
                                    esxi_password=vCenter_password)

                while vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                         username=vCenter_user,
                                         password=vCenter_password,
                                         vm_name=clone_name) == False:
                    print("VM Tools status kontrol ediliyor")
                    time.sleep(3)

                vm_tools_status = vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                                     username=vCenter_user,
                                                     password=vCenter_password,
                                                     vm_name=clone_name)

                counter += 1

                if vm_tools_status:

                    if pfms_config_type == "SAPaaS":

                        if vm_config_lists_OperatingSystemInformation == "Windows":
                            execute_sapaas_disk_to_centos.main(vCenter_host_ip=vCenter_host_ip,
                                                               vCenter_user=vCenter_user,
                                                               vCenter_password=vCenter_password,
                                                               vm_name=clone_name,
                                                               disk_mount_location=disk_mount_location)

                            disk_mount_location = disk_mount_location + str(counter)

                        elif vm_config_lists_OperatingSystemInformation == "Linux":
                            execute_disk_to_linux.main(vm_name=clone_name,
                                                       esxi_host_ip=vCenter_host_ip,
                                                       esxi_user=vCenter_user,
                                                       esxi_password=vCenter_password,
                                                       os_user="root",
                                                       os_password="111111")


                    elif pfms_config_type == "IaaS":

                        if vm_config_lists_OperatingSystemInformation == "Windows":
                            execute_disk_to_windows.main(target_vm_name=clone_name,
                                                        esxi_host_ip=vCenter_host_ip,
                                                        esxi_user=vCenter_user,
                                                        esxi_password=vCenter_password,
                                                        label="Glass_House_Disk_" + str(counter),
                                                        assign_letter=current_letter,
                                                        disk_number=counter)

                            current_letter = allowed_letters[allowed_letters.index(current_letter) + 1]

                        elif vm_config_lists_OperatingSystemInformation == "Linux":
                            execute_disk_to_linux.main(vm_name=clone_name,
                                                       esxi_host_ip=vCenter_host_ip,
                                                       esxi_user=vCenter_user,
                                                       esxi_password=vCenter_password,
                                                       os_user="root",
                                                       os_password="111111")

                else:
                    while vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                             username=vCenter_user,
                                             password=vCenter_password,
                                             vm_name=clone_name) == False:
                        time.sleep(3)

                    vm_tools_status = vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                                         username=vCenter_user,
                                                         password=vCenter_password,
                                                         vm_name=clone_name)
                    if vm_tools_status:
                        if pfms_config_type == "SAPaaS":
                            if vm_config_lists_OperatingSystemInformation == "Windows":
                                execute_sapaas_disk_to_centos.main(vCenter_host_ip=vCenter_host_ip,
                                                               vCenter_user=vCenter_user,
                                                               vCenter_password=vCenter_password,
                                                               vm_name=clone_name,
                                                               disk_mount_location=disk_mount_location)
                            disk_mount_location = disk_mount_location + str(counter)
                        elif pfms_config_type == "IaaS":
                            if vm_config_lists_OperatingSystemInformation == "Windows":
                                execute_disk_to_windows.main(target_vm_name=clone_name,
                                                             esxi_host_ip=vCenter_host_ip,
                                                             esxi_user=vCenter_user,
                                                             esxi_password=vCenter_password,
                                                             label="Glass_House_Disk_" + str(counter),
                                                             assign_letter=current_letter,
                                                             disk_number=counter)
                                current_letter = allowed_letters[allowed_letters.index(current_letter) + 1]
                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                execute_disk_to_linux.main(vm_name=clone_name,
                                                           esxi_host_ip=vCenter_host_ip,
                                                           esxi_user=vCenter_user,
                                                           esxi_password=vCenter_password,
                                                           os_user="root",
                                                           os_password="111111")
                        break

                if not vm_tools_status:
                    raise Exception("VM Tools status could not be verified after retrying.")


        print("Create işlemi tamamlandı")
if __name__ == "__main__":
    main()
