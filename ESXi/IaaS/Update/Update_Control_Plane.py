from ESXi.IaaS.Update.DiskOps import disk_ops_main

def main():
    vm_name = "Deneme_ubuntu_bulent"

    # esxi host bilgileri
    esxi_host_ip = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    update_mod = input("1- Disk_Ops\n2- Network_Ops\n3- Reconfg_Ops\n4- Registiration_Ops\n5- execute_commands\n")

    if update_mod == "1":
        disk_ops_main.main(vm_name=vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)


if __name__ == "__main__":
    main()

