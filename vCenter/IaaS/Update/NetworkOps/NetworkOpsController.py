from vCenter.IaaS.Connections.vSphere_connection import *
from vCenter.IaaS.Update.NetworkOps.AddNetworkAdapter import add_network_adapter
from vCenter.IaaS.Update.NetworkOps.CheckNetworkAdapter import check_network_adapter_existence
from vCenter.IaaS.Update.NetworkOps.DeleteNetworkAdapter import delete_network_adapter
from vCenter.IaaS.Update.NetworkOps.SetIPAdress import execute_ipAddress_to_linux
from vCenter.IaaS.Update.NetworkOps.SetIPAdress import execute_ipAddress_windows
from vCenter.IaaS.Update import GuestOsFamilyFinder

def WaitForTask(task):
    """Bir vSphere görevi tamamlanana kadar bekler ve güncellemeler sağlar."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Görev başarıyla tamamlandı.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Hata: {task.info.error}")
            task_done = True

def main(vm_name, vCenter_host_ip, vCenter_user, vCenter_password):

    os_family = GuestOsFamilyFinder.main(vm_name=vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user,
                                         vCenter_password=vCenter_password)

    result = check_network_adapter_existence.main()
    network_adapter_existence_value = result[0]
    device_label = result[1]

    network_ops_mod = input("1- Add_Network_Adapter\n2- Delete_Network_Adapter\n3-Set Ip Address\n4-Chech Network Adapter Existence\n")

    if network_ops_mod == "1":
        add_network_adapter.main(vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

    elif network_ops_mod == "2":
        delete_network_adapter.main(vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

    elif network_ops_mod == "3":
        if network_adapter_existence_value is True:

            service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)
            vm_to_reconfigure = get_vm_by_name(content, vm_name)

            if vm_to_reconfigure.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
                task = vm_to_reconfigure.PowerOnVM_Task()
                WaitForTask(task)

            #TODO: buraya şimdilik Windows ve Linux için ayrı ayrı yazıldı. Diğer işletim sistemleri için de ayrı ayrı yazılabilir.
            if os_family == "Linux":
                execute_ipAddress_to_linux.main(vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)
            elif os_family == "Windows":
                execute_ipAddress_windows.main(vm_name, vCenter_host_ip=vCenter_host_ip, vCenter_user=vCenter_user, vCenter_password=vCenter_password)

    elif network_ops_mod == "4":
        if network_adapter_existence_value is True:
            print(f"{device_label} ağ adaptörü var.")
        else:
            print("Ağ adaptörü yok.")

    else:
        print("Geçersiz işlem.")