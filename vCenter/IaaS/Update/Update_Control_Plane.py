from ESXi.IaaS.Update.DiskOps import DiskOpsController
from ESXi.IaaS.Update.NetworkOps import NetworkOpsController
from ESXi.IaaS.Update.Reconfig import reconfig_vm, rename_vm
from ESXi.IaaS.Update.Registiration_Ops import registry_vm, unRegister_Vm

def main():
    vm_name = "Clone-SUSE-Temp-15-3"

    # esxi host bilgileri
    esxi_host_ip = "10.14.45.10"
    esxi_user = "administrator@vsphere.local"
    esxi_password = "Aa112233!"

    update_mod = input("1- Disk_Ops\n2- Network_Ops\n3-Reconfg_Ops\n4-Register VM\n5-UnRegister VM\n6-Rename VM\n7-execute_commands\n")

    if update_mod == "1":
        DiskOpsController.main(vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif update_mod == "2":
        NetworkOpsController.main(vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif update_mod == "3":
        target_cpu_count = 2  # Modify with the desired CPU count
        target_memory_mb = 4096  # Modify with the desired memory size in MB
        target_disk_size_gb = 48  # Modify with the desired disk size in GB

        reconfig_vm.main(vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password, target_cpu_count=target_cpu_count, target_memory_mb=target_memory_mb, target_disk_size_gb=target_disk_size_gb)

    elif update_mod == "4":
        registry_vm_name = input("Registry VM Name: ")
        registry_vm.main(registry_vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password, copied_folder_name=vm_name)

    elif update_mod == "5":
        unRegister_Vm.main(vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif update_mod == "6":
        new_vm_name = input("New VM Name: ")
        rename_vm.main(old_vm_name=vm_name, new_vm_name=new_vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

if __name__ == "__main__":
    main()

