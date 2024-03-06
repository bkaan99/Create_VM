from vCenter.IaaS.Update.DiskOps import DiskOpsController
from vCenter.IaaS.Update.NetworkOps import NetworkOpsController
from vCenter.IaaS.Update.Reconfig import reconfig_vm, rename_vm
from vCenter.IaaS.Update.Registiration_Ops import registry_vm, unRegister_Vm

def main():
    vm_name = "BilgeKaanGurgen"

    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    update_mod = input("1- Disk_Ops\n2- Network_Ops\n3-Reconfg_Ops\n4-Register VM\n5-UnRegister VM\n6-Rename VM\n7-execute_commands\n")

    if update_mod == "1":
        DiskOpsController.main(vm_name=vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

    elif update_mod == "2":
        NetworkOpsController.main(vm_name=vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

    elif update_mod == "3":
        target_cpu_count = 2  # Modify with the desired CPU count
        target_memory_mb = 4096  # Modify with the desired memory size in MB
        target_disk_size_gb = 48  # Modify with the desired disk size in GB

        reconfig_vm.main(vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password, clone_name=vm_name, cpu_count=target_cpu_count, memory_mb=target_memory_mb, disk_size_gb=target_disk_size_gb)

    elif update_mod == "4":
        registry_vm_name = input("Registry VM Name: ")
        registry_vm.main(registry_vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password, copied_folder_name=vm_name)

    elif update_mod == "5":
        unRegister_Vm.main(vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

    elif update_mod == "6":
        new_vm_name = input("New VM Name: ")
        rename_vm.main(old_vm_name=vm_name, new_vm_name=new_vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

if __name__ == "__main__":
    main()

