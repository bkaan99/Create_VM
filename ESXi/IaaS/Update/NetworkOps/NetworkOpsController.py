from ESXi.IaaS.Update.NetworkOps.AddNetworkAdapter import add_network_adapter
from ESXi.IaaS.Update.NetworkOps.CheckNetworkAdapter import check_network_adapter_existence
from ESXi.IaaS.Update.NetworkOps.DeleteNetworkAdapter import delete_network_adapter
from ESXi.IaaS.Update.NetworkOps.SetIPAdress import execute_ipAddress_to_linux
from ESXi.IaaS.Update.NetworkOps.SetIPAdress import execute_ipAddress_windows


def find_os_family():

    # TODO: buraya os faqmily bulma işlemi yapılacak. Esxi bağlanıp family bilgisi alınacak
    # find os family
    # os_family = "windows" or "linux"
    os_family = "linux"
    return os_family

def main(vm_name, esxi_host_ip, esxi_user, esxi_password):

    result = check_network_adapter_existence.main()
    network_adapter_existence_value = result[0]
    device_label = result[1]

    network_ops_mod = input("1- Add_Network_Adapter\n2- Delete_Network_Adapter\n3-Set Ip Address\n4-Chech Network Adapter Existence\n")

    if network_ops_mod == "1":
        add_network_adapter.main(vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif network_ops_mod == "2":
        delete_network_adapter.main(vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif network_ops_mod == "3":
        if network_adapter_existence_value == True:
            if find_os_family() == "linux":
                execute_ipAddress_to_linux.main(vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)
            elif find_os_family() == "windows":
                execute_ipAddress_windows.main(vm_name, esxi_host_ip=esxi_host_ip, esxi_user=esxi_user, esxi_password=esxi_password)

    elif network_ops_mod == "4":
        if network_adapter_existence_value == True:
            print(f"{device_label} ağ adaptörü var.")
        else:
            print(f"Ağ adaptörü yok.")


if __name__ == "__main__":
    main()