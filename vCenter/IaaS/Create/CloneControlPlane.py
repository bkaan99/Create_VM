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
import createitsmtaskLast
import updateItsmTask


def connect_to_postgres():
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()
    return connectionForPostgres, cursorForPostgres

def diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList):
    for f in range(len(diskSetSAPaaSTaskList)):
        updateItsmTask.updateTaskItsm(diskSetSAPaaSTaskList[f][0], diskSetSAPaaSTaskList[f][1],
                                      1202,
                                      vmid)

def assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList):
    for f in range(len(assignIpToIaasVmTaskList)):
        updateItsmTask.updateTaskItsm(assignIpToIaasVmTaskList[f][0], assignIpToIaasVmTaskList[f][1],
                                      1202,
                                      vmid)

def delete_itsm_tasks(vmidToDelete):
    connectionForPostgres, cursorForPostgres = connect_to_postgres()
    query_to_execute_delete_tasks = "delete from kr_create_task where vmlist_id="+str(vmidToDelete)
    cursorForPostgres.execute(query_to_execute_delete_tasks)
    connectionForPostgres.commit()

def get_itsm_values(vmidToGetInfo, operationCode):
    connectionForPostgres, cursorForPostgres = connect_to_postgres()
    query_to_execute ="select description, title, matchedpytocode from kr_create_task kct where vmlist_id = "+str(vmidToGetInfo)+" and matchedpytocode = '"+str(operationCode)+"' and is_deleted = false;"
    #query_to_execute = "select kstd.description, ktd.taskname, ktd.matchedpytocode from kr_service_task_definition kstd inner join kr_task_definition ktd on kstd.id = ktd.service_task_definition_id where kstd.id in (select kvl.servicetaskdefinition_id from kr_vm_list kvl where kvl.id = "+str(vmidToGetInfo)+" and kvl.is_deleted =false limit 1 ) and ktd.is_deleted = false and kstd.is_deleted = false and matchedpytocode = '"+str(operationCode)+"'"
    cursorForPostgres.execute(query_to_execute)
    itsm_data_list = cursorForPostgres.fetchall()
    return itsm_data_list


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

        #ITSM task kontrolü
        delete_itsm_tasks(vmid)
        createitsmtaskLast.createTaskItsm(vmid)

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


        createIaasVMTaskList = get_itsm_values(vmid, 1)
        for f in range(len(createIaasVMTaskList)):
            updateItsmTask.updateTaskItsm(createIaasVMTaskList[f][0], createIaasVMTaskList[f][1], 1202, vmid)

        updateIaasVMTaskList = get_itsm_values(vmid, 2)
        for f in range(len(updateIaasVMTaskList)):
            updateItsmTask.updateTaskItsm(updateIaasVMTaskList[f][0], updateIaasVMTaskList[f][1], 1202,
                                          vmid)

        startIaasVmTaskList = get_itsm_values(vmid, 3)
        for f in range(len(startIaasVmTaskList)):
            updateItsmTask.updateTaskItsm(startIaasVmTaskList[f][0], startIaasVmTaskList[f][1], 1202, vmid)



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


                assignIpToIaasVmTaskList = get_itsm_values(vmid, 4)

                if vm_tools_status:
                    if vm_config_lists_OperatingSystemInformation == "Windows":
                        execute_ipAddress_windows.main(vm_name=clone_name,
                                                       vCenter_host_ip=vCenter_host_ip,
                                                       vCenter_user=vCenter_user,
                                                       vCenter_password=vCenter_password,
                                                       ipAddress=vm_config_lists_IpAdress)

                        assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList)

                    elif vm_config_lists_OperatingSystemInformation == "Linux":
                        execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                        vCenter_host_ip=vCenter_host_ip,
                                                        vCenter_user=vCenter_user,
                                                        vCenter_password=vCenter_password,
                                                        ipAddress=vm_config_lists_IpAdress)

                        assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList)

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

                        assignIpToIaasVmTaskList = get_itsm_values(vmid, 4)

                        if vm_tools_status:
                            if vm_config_lists_OperatingSystemInformation == "Windows":
                                execute_ipAddress_windows.main(vm_name=clone_name,
                                                               vCenter_host_ip=vCenter_host_ip,
                                                               vCenter_user=vCenter_user,
                                                               vCenter_password=vCenter_password,
                                                               ipAddress=vm_config_lists_IpAdress)

                                #itsm task list
                                assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList)


                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                                vCenter_host_ip=vCenter_host_ip,
                                                                vCenter_user=vCenter_user,
                                                                vCenter_password=vCenter_password,
                                                                ipAddress=vm_config_lists_IpAdress)

                                #itsm task list
                                assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList)

                            break
                        retry_count += 1

                if not vm_tools_status:
                    raise Exception("VM Tools status could not be verified after retrying.")

            elif network_adapter_existence_value == False:
                add_network_adapter.main(vm_name_to_reconfigure=clone_name,
                                         vCenter_host_ip=vCenter_host_ip,
                                         vCenter_user=vCenter_user,
                                         vCenter_password=vCenter_password)

                # itsm task list
                assignIpToIaasVmTaskList = get_itsm_values(vmid, 4)

                if vm_config_lists_OperatingSystemInformation == "Windows":
                    execute_ipAddress_windows.main(vm_name=clone_name,
                                                   vCenter_host_ip=vCenter_host_ip,
                                                   vCenter_user=vCenter_user,
                                                   vCenter_password=vCenter_password,
                                                   ipAddress=vm_config_lists_IpAdress)

                    # itsm task list
                    assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList)


                elif vm_config_lists_OperatingSystemInformation == "Linux":
                    execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                    vCenter_host_ip=vCenter_host_ip,
                                                    vCenter_user=vCenter_user,
                                                    vCenter_password=vCenter_password,
                                                    ipAddress=vm_config_lists_IpAdress)

                    # itsm task list
                    assignIpToIaasVmTaskList_For(vmid, assignIpToIaasVmTaskList)

        # add disk to VM
        if len(other_disk_list) > 0:
            allowed_letters = string.ascii_uppercase[4:]  # "E" harfinden başlayarak "Z" harfine kadar olan harfler
            current_letter = allowed_letters[0]
            disk_number_windows = 0
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

                disk_number_windows += 1

                diskSetSAPaaSTaskList = get_itsm_values(vmid, 5)


                if vm_tools_status:

                    if pfms_config_type == "SAPaaS":

                        if vm_config_lists_OperatingSystemInformation == "Windows":
                            execute_sapaas_disk_to_centos.main(vCenter_host_ip=vCenter_host_ip,
                                                               vCenter_user=vCenter_user,
                                                               vCenter_password=vCenter_password,
                                                               vm_name=clone_name,
                                                               disk_mount_location=disk_mount_location)

                            disk_mount_location = disk_mount_location + str(disk_number_windows)

                            # itsm task list
                            diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)

                        elif vm_config_lists_OperatingSystemInformation == "Linux":
                            execute_disk_to_linux.main(vm_name=clone_name,
                                                       esxi_host_ip=vCenter_host_ip,
                                                       esxi_user=vCenter_user,
                                                       esxi_password=vCenter_password,
                                                       os_user="root",
                                                       os_password="111111")

                            # itsm task list
                            diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)

                    elif pfms_config_type == "IaaS":

                        if vm_config_lists_OperatingSystemInformation == "Windows":
                            execute_disk_to_windows.main(target_vm_name=clone_name,
                                                        esxi_host_ip=vCenter_host_ip,
                                                        esxi_user=vCenter_user,
                                                        esxi_password=vCenter_password,
                                                        label="Glass_House_Disk_" + str(disk_number_windows),
                                                        assign_letter=current_letter,
                                                        disk_number=disk_number_windows)

                            current_letter = allowed_letters[allowed_letters.index(current_letter) + 1]

                            # itsm task list
                            diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)

                        elif vm_config_lists_OperatingSystemInformation == "Linux":
                            execute_disk_to_linux.main(vm_name=clone_name,
                                                       esxi_host_ip=vCenter_host_ip,
                                                       esxi_user=vCenter_user,
                                                       esxi_password=vCenter_password,
                                                       os_user="root",
                                                       os_password="111111")

                            # itsm task list
                            diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)

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

                            disk_mount_location = disk_mount_location + str(disk_number_windows)

                            # itsm task list
                            diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)

                        elif pfms_config_type == "IaaS":
                            if vm_config_lists_OperatingSystemInformation == "Windows":
                                execute_disk_to_windows.main(target_vm_name=clone_name,
                                                             esxi_host_ip=vCenter_host_ip,
                                                             esxi_user=vCenter_user,
                                                             esxi_password=vCenter_password,
                                                             label="Glass_House_Disk_" + str(disk_number_windows),
                                                             assign_letter=current_letter,
                                                             disk_number=disk_number_windows)
                                current_letter = allowed_letters[allowed_letters.index(current_letter) + 1]

                                #itsm task list
                                diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)

                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                execute_disk_to_linux.main(vm_name=clone_name,
                                                           esxi_host_ip=vCenter_host_ip,
                                                           esxi_user=vCenter_user,
                                                           esxi_password=vCenter_password,
                                                           os_user="root",
                                                           os_password="111111")

                                #itsm task list
                                diskSetSAPaaSTaskList_For(vmid, diskSetSAPaaSTaskList)
                        break

                if not vm_tools_status:
                    raise Exception("VM Tools status could not be verified after retrying.")

        print("Create işlemi tamamlandı")

if __name__ == "__main__":
    main()
