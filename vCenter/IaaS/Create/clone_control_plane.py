## Sunucu için eklenmesi gereken sys path.
# import sys
# sys.path.append('/home/gardiyan/Gardiyan/Server/pfms/apache-karaf-5005/GH-Plugins')
import string
import time
from vCenter.IaaS.Connections.db_connection import *
from vCenter.IaaS.Create import clone_from_template
from vCenter.IaaS.ExternelFiles import check_vm_os_family, vmtoolsstatus, get_id_list_controller
from vCenter.IaaS.Update.DiskOps.AddDisk import add_disk_to_vm
from vCenter.IaaS.Update.DiskOps.SetDisk import execute_disk_to_windows, execute_disk_to_linux, execute_sapaas_disk_to_centos
from vCenter.IaaS.Update.NetworkOps.AddNetworkAdapter import add_network_adapter
from vCenter.IaaS.Update.NetworkOps.CheckNetworkAdapter import check_network_adapter_existence
from vCenter.IaaS.Update.NetworkOps.SetIPAdress import execute_ipAddress_windows, execute_ipAddress_to_linux
from vCenter.ITSM_Integration import createitsmtaskLast, updateItsmTask


def delete_itsm_tasks(vmidToDelete):
    connectionForPostgres, cursorForPostgres = connect_Postgres()
    query_to_execute_delete_tasks = "delete from kr_create_task where vmlist_id="+str(vmidToDelete)
    cursorForPostgres.execute(query_to_execute_delete_tasks)
    connectionForPostgres.commit()

def get_itsm_values(vmidToGetInfo, operationCode):
    connectionForPostgres, cursorForPostgres = connect_Postgres()
    query_to_execute ="select description, title, matchedpytocode from kr_create_task kct where vmlist_id = "+str(vmidToGetInfo)+" and matchedpytocode = '"+str(operationCode)+"' and is_deleted = false;"
    #query_to_execute = "select kstd.description, ktd.taskname, ktd.matchedpytocode from kr_service_task_definition kstd inner join kr_task_definition ktd on kstd.id = ktd.service_task_definition_id where kstd.id in (select kvl.servicetaskdefinition_id from kr_vm_list kvl where kvl.id = "+str(vmidToGetInfo)+" and kvl.is_deleted =false limit 1 ) and ktd.is_deleted = false and kstd.is_deleted = false and matchedpytocode = '"+str(operationCode)+"'"
    cursorForPostgres.execute(query_to_execute)
    itsm_data_list = cursorForPostgres.fetchall()
    return itsm_data_list

def task_sender(stage_name, vmid, operationCode, cookie, task_mod):
    if task_mod == 1:
        stage_name = get_itsm_values(vmid, operationCode=operationCode)
        for f in range(len(stage_name)):
            updateItsmTask.updateTaskItsm(stage_name[f][0],
                                          stage_name[f][1],
                                          1202,
                                          vmid,
                                          cookie=cookie)

    elif task_mod == 2:
        for f in range(len(stage_name)):
            updateItsmTask.updateTaskItsm(stage_name[f][0],
                                          stage_name[f][1],
                                          1202,
                                          vmid,
                                          cookie=cookie)


def main():
    print("IAAS Create işlemi başlatıldı")

    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    #vm id arguments
    vmIdList = get_id_list_controller.get_id_list()

    #get cookie for itsm task
    cookie = createitsmtaskLast.seleniumItsm()

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

        #get pfms config type / SAPaaS - IaaS
        pfms_config_type = vm_config_lists[12]

        #get first disk config
        vm_disk_list = get_first_disik_Config(vmid)
        vm_all_disks =vm_disk_list[0]
        vm_first_disk_size_gb = int(vm_disk_list[0][0])
        vm_all_disks.pop(0)

        #get first disk mods
        vm_disk_mods = vm_disk_list[1]
        vm_first_disk_mod = vm_disk_mods[0]
        vm_disk_mods.pop(0)

        #get other disk configs
        other_disk_list = vm_all_disks
        other_disk_mods = vm_disk_mods

        #get template name
        template_name = check_vm_os_family.main(vm_config_lists_OperatingSystemInformation, vm_config_lists_OperatingSystemVersion)
        clone_name = vm_config_lists_VmName

        # #ITSM task kontrolü

        delete_itsm_tasks(vmid)
        createitsmtaskLast.createTaskItsm(vmid, cookie= cookie)


        ## Clone VM from template
        clone_from_template.main(vCenter_host_ip=vCenter_host_ip,
                                 vCenter_user=vCenter_user,
                                 vCenter_password=vCenter_password,
                                 template_name=template_name,
                                 clone_name=clone_name,
                                 disk_size_gb=vm_first_disk_size_gb,
                                 disk_mode=vm_first_disk_mod,
                                 memory_mb=vm_config_lists_RamSize,
                                 cpu_count=vm_config_lists_Cpu)

        print("VM Tools Kontrol ediliyor.")
        while vmtoolsstatus.main(vCenterIP=vCenter_host_ip, username=vCenter_user,
                                 password=vCenter_password,
                                 vm_name=clone_name) == False:
            print("VM Tools status kontrol döngüsü başlatıldı...")
            time.sleep(3)

        print("VM Tools status kontrol döngüsü tamamlandı.")

        #task send number 1
        task_sender(stage_name="_", vmid=vmid, operationCode=1, cookie=cookie, task_mod=1)

        #task send number 2
        task_sender(stage_name="_", vmid=vmid, operationCode=2, cookie=cookie , task_mod=1)

        #task send number 3
        task_sender(stage_name="_", vmid=vmid, operationCode=3, cookie=cookie, task_mod=1)

        # task send number 6
        task_sender(stage_name="_", vmid=vmid, operationCode=6, cookie=cookie, task_mod=1)

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

                        # itsm task list
                        task_sender(stage_name=assignIpToIaasVmTaskList, vmid=vmid, operationCode=4,
                                    cookie=cookie,task_mod=2)

                    elif vm_config_lists_OperatingSystemInformation == "Linux":
                        execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                        vCenter_host_ip=vCenter_host_ip,
                                                        vCenter_user=vCenter_user,
                                                        vCenter_password=vCenter_password,
                                                        ipAddress=vm_config_lists_IpAdress)

                        # itsm task list
                        task_sender(stage_name=assignIpToIaasVmTaskList, vmid=vmid, operationCode=4,
                                    cookie=cookie,task_mod=2)

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

                                # itsm task list
                                task_sender(stage_name=assignIpToIaasVmTaskList, vmid=vmid, operationCode=4,
                                            cookie=cookie, task_mod=2)


                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                                vCenter_host_ip=vCenter_host_ip,
                                                                vCenter_user=vCenter_user,
                                                                vCenter_password=vCenter_password,
                                                                ipAddress=vm_config_lists_IpAdress)

                                # itsm task list
                                task_sender(stage_name=assignIpToIaasVmTaskList, vmid=vmid, operationCode=4,
                                            cookie=cookie, task_mod=2)

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
                    task_sender(stage_name=assignIpToIaasVmTaskList, vmid=vmid, operationCode=4,
                                cookie=cookie, task_mod=2)

                elif vm_config_lists_OperatingSystemInformation == "Linux":
                    execute_ipAddress_to_linux.main(vm_name=clone_name,
                                                    vCenter_host_ip=vCenter_host_ip,
                                                    vCenter_user=vCenter_user,
                                                    vCenter_password=vCenter_password,
                                                    ipAddress=vm_config_lists_IpAdress)

                    # itsm task list
                    task_sender(stage_name=assignIpToIaasVmTaskList, vmid=vmid, operationCode=4,
                                cookie=cookie, task_mod=2)

        # add disk to VM
        if len(other_disk_list) > 0:
            allowed_letters = string.ascii_uppercase[4:]  # "E" harfinden başlayarak "Z" harfine kadar olan harfler
            current_letter = allowed_letters[0]
            disk_number_windows = 0
            disk_mount_location = "hana/shared"
            for disk_size_gb, disk_mods in zip(other_disk_list, other_disk_mods):

                add_disk_to_vm.main(vm_name_to_reconfigure=clone_name,
                                    target_disk_size_gb=disk_size_gb,
                                    disk_mode=vm_disk_mods,
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
                            print("SAPaaS Windows disk set işlemi yapılıyor.")
                            execute_disk_to_windows.main(target_vm_name=clone_name,
                                                         esxi_host_ip=vCenter_host_ip,
                                                         esxi_user=vCenter_user,
                                                         esxi_password=vCenter_password,
                                                         label="Glass_House_Disk_" + str(disk_number_windows),
                                                         assign_letter=current_letter,
                                                         disk_number=disk_number_windows)

                            disk_mount_location = disk_mount_location + str(disk_number_windows)
                            time.sleep(5)

                            #itsm task list
                            task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                        cookie=cookie, task_mod=2)

                        elif vm_config_lists_OperatingSystemInformation == "Linux":
                            print("SAPaaS Linux disk set işlemi yapılıyor.")
                            execute_sapaas_disk_to_centos.main(vCenter_host_ip=vCenter_host_ip,
                                                               vCenter_user=vCenter_user,
                                                               vCenter_password=vCenter_password,
                                                               vm_name=clone_name,
                                                               disk_mount_location=disk_mount_location,
                                                               reboot_guest=True)

                            #itsm task list
                            task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                        cookie=cookie, task_mod=2)

                    elif pfms_config_type == "IaaS":

                        if vm_config_lists_OperatingSystemInformation == "Windows":
                            print("IaaS Windows disk set işlemi yapılıyor.")
                            execute_disk_to_windows.main(target_vm_name=clone_name,
                                                        esxi_host_ip=vCenter_host_ip,
                                                        esxi_user=vCenter_user,
                                                        esxi_password=vCenter_password,
                                                        label="Glass_House_Disk_" + str(disk_number_windows),
                                                        assign_letter=current_letter,
                                                        disk_number=disk_number_windows)

                            current_letter = allowed_letters[allowed_letters.index(current_letter) + 1]
                            time.sleep(5)

                            # itsm task list
                            task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                        cookie=cookie, task_mod=2)

                        elif vm_config_lists_OperatingSystemInformation == "Linux":
                            print("IaaS Linux disk set işlemi yapılıyor.")
                            execute_disk_to_linux.main(vm_name=clone_name,
                                                       esxi_host_ip=vCenter_host_ip,
                                                       esxi_user=vCenter_user,
                                                       esxi_password=vCenter_password,
                                                       os_user="root",
                                                       os_password="111111")

                            # itsm task list
                            task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                        cookie=cookie, task_mod=2)

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
                                print("SAPaaS Windows disk set işlemi yapılıyor.")
                                execute_disk_to_windows.main(target_vm_name=clone_name,
                                                             esxi_host_ip=vCenter_host_ip,
                                                             esxi_user=vCenter_user,
                                                             esxi_password=vCenter_password,
                                                             label="Glass_House_Disk_" + str(disk_number_windows),
                                                             assign_letter=current_letter,
                                                             disk_number=disk_number_windows)

                                disk_mount_location = disk_mount_location + str(disk_number_windows)
                                time.sleep(5)

                                #itsm task list
                                task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                            cookie=cookie, task_mod=2)

                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                print("SAPaaS Linux disk set işlemi yapılıyor.")
                                execute_sapaas_disk_to_centos.main(vCenter_host_ip=vCenter_host_ip,
                                                                   vCenter_user=vCenter_user,
                                                                   vCenter_password=vCenter_password,
                                                                   vm_name=clone_name,
                                                                   disk_mount_location=disk_mount_location,
                                                                   reboot_guest=True)

                                #itsm task list
                                task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                            cookie=cookie, task_mod=2)


                        elif pfms_config_type == "IaaS":
                            if vm_config_lists_OperatingSystemInformation == "Windows":
                                print("IaaS Windows disk set işlemi yapılıyor.")
                                execute_disk_to_windows.main(target_vm_name=clone_name,
                                                             esxi_host_ip=vCenter_host_ip,
                                                             esxi_user=vCenter_user,
                                                             esxi_password=vCenter_password,
                                                             label="Glass_House_Disk_" + str(disk_number_windows),
                                                             assign_letter=current_letter,
                                                             disk_number=disk_number_windows)
                                current_letter = allowed_letters[allowed_letters.index(current_letter) + 1]
                                time.sleep(5)

                                #itsm task list
                                task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                            cookie=cookie, task_mod=2)

                            elif vm_config_lists_OperatingSystemInformation == "Linux":
                                print("IaaS Linux disk set işlemi yapılıyor.")
                                execute_disk_to_linux.main(vm_name=clone_name,
                                                           esxi_host_ip=vCenter_host_ip,
                                                           esxi_user=vCenter_user,
                                                           esxi_password=vCenter_password,
                                                           os_user="root",
                                                           os_password="111111")

                                #itsm task list
                                task_sender(stage_name=diskSetSAPaaSTaskList, vmid=vmid, operationCode=5,
                                            cookie=cookie, task_mod=2)

                        break

                if not vm_tools_status:
                    raise Exception("VM Tools status could not be verified after retrying.")

        print("Create işlemi tamamlandı")

if __name__ == "__main__":
    main()
