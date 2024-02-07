import time
from ESXi.IaaS.Update import GuestOsFamilyFinder
from ESXi.IaaS.Update.DiskOps.AddDisk import add_disk_to_vm, execute_disk_to_windows, execute_disk_to_linux
from ESXi.IaaS.Update.DiskOps.DeleteDisk import delete_disk_to_vm
from ESXi.IaaS.Update.DiskOps.ResizeDisk import resizeDisk
from ESXi.IaaS.Update.DiskOps.SetDisk import execute_createSWAP_disk_to_linux

def main(vm_name, esxi_host_ip, esxi_user, esxi_password):

    os_family = GuestOsFamilyFinder.main(vm_name_to_reconfigure=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    #TODO: buraya disk işlemleri için gerekli bilgiler alınacak
    target_disk_size = 2  # GB

    disk_mod = input("1- Add_Disk\n2- Delete_Disk\n3- Resize_Disk\n")

    #Add Disk
    if disk_mod == "1":
        add_disk_to_vm.main(vm_name_to_reconfigure=vm_name, target_disk_size_gb=target_disk_size, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)
        time.sleep(10)

        # TODO: buraya şimdilik Windows ve Linux için ayrı ayrı yazıldı. Diğer işletim sistemleri için de ayrı ayrı yazılabilir.
        if os_family == "Windows":
            execute_disk_to_windows.main(target_vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user,
                                         esxi_password=esxi_password)
        elif os_family == "Linux":
            execute_disk_to_linux.main(vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user,
                                       esxi_password=esxi_password)
    #Delete Disk
    elif disk_mod == "2":
        delete_disk_to_vm.main(vm_name_to_reconfigure=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user,
                               esxi_password=esxi_password)
    #Resize Disk
    elif disk_mod == "3":
        resizeDisk.main(vm_name_to_reconfigure=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user,
                        esxi_password=esxi_password)

    #swap alanı oluşturma istiyor musunuz?
    swap_mod = input("1- Yes\n2- No\n")
    if swap_mod == "1":
        execute_createSWAP_disk_to_linux.main(vm_name, esxi_host_ip, esxi_user, esxi_password)