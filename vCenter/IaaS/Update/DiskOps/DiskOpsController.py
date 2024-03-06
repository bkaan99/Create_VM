from vCenter.IaaS.ExternelFiles import vmtoolsstatus
from vCenter.IaaS.Update import GuestOsFamilyFinder
from vCenter.IaaS.Update.DiskOps.AddDisk import add_disk_to_vm, disk_executor_windows_with_windows, disk_executor_linux_with_linux
from vCenter.IaaS.Update.DiskOps.DeleteDisk import delete_disk_to_vm
from vCenter.IaaS.Update.DiskOps.ResizeDisk import resizeDisk
from vCenter.IaaS.Update.DiskOps.SetDisk import execute_createSWAP_disk_to_linux
import time

def main(vm_name, vCenter_host_ip, vCenter_user, vCenter_password):

    disk_mod = input("1- Add_Disk\n2- Delete_Disk\n3- Resize_Disk\n")

    target_disk_size = 1  # GB

    #Add Disk
    if disk_mod == "1":
        #FIXME: disk mode ve disk size değerleri dinamik gelecek.

        add_disk_to_vm.main(vm_name_to_reconfigure=vm_name, target_disk_size_gb=target_disk_size, disk_mode="persistent",
                            vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

        while vmtoolsstatus.main(vCenterIP=vCenter_host_ip,
                                 username=vCenter_user,
                                 password=vCenter_password,
                                 vm_name=vm_name) == False:
            print("VMTools is not running. Waiting for 3 seconds...")
            time.sleep(3)

        os_family = GuestOsFamilyFinder.main(vm_name_to_reconfigure=vm_name, esxi_host_ip=vCenter_host_ip,
                                             esxi_user=vCenter_user, esxi_password=vCenter_password)

        if os_family == "Windows":
            disk_executor_windows_with_windows.main(target_vm_name=vm_name, esxi_host_ip=vCenter_host_ip, esxi_user=vCenter_user,
                                         esxi_password=vCenter_password)
        elif os_family == "Linux":
            disk_executor_linux_with_linux.main(vm_name=vm_name, esxi_host_ip=vCenter_host_ip, esxi_user=vCenter_user,
                                       esxi_password=vCenter_password)


    #Delete Disk
    elif disk_mod == "2":
        delete_disk_to_vm.main(vm_name_to_reconfigure=vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user,
                               vCenter_password=vCenter_password, hard_disk_name_to_delete="Hard disk 2")


    #Resize Disk
    elif disk_mod == "3":
        resizeDisk.main(vm_name_to_reconfigure=vm_name, esxi_host_ip=vCenter_host_ip, esxi_user=vCenter_user,
                        esxi_password=vCenter_password)


    #swap alanı oluşturma istiyor musunuz?
    swap_mod = input("1- Yes\n2- No\n")
    if swap_mod == "1":
        execute_createSWAP_disk_to_linux.main(vm_name, vCenter_host_ip, vCenter_user, vCenter_password)