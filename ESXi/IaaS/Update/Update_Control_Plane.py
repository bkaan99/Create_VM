from ESXi.IaaS.Update.DiskOps import DiskOpsController
from ESXi.IaaS.Update.NetworkOps import NetworkOpsController


def main():
    vm_name = "Clone-SUSE-Temp-15-3"

    # esxi host bilgileri
    esxi_host_ip = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    update_mod = input("1- Disk_Ops\n2- Network_Ops\n3- Reconfg_Ops\n4- Registiration_Ops\n5- execute_commands\n")

    if update_mod == "1":
        DiskOpsController.main(vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif update_mod == "2":
        NetworkOpsController.main(vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)


if __name__ == "__main__":
    main()

