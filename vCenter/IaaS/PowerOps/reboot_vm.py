from pyVim.connect import Disconnect
from pyVmomi import vim
import time
from vCenter.IaaS.Connections.vSphere_connection import create_vsphere_connection, get_vm_by_name


def reboot_vm(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        task = vm.RebootGuest()
        if task:
            WaitForTask(task)
            print("VM is rebooting...")
        else:
            print("Failed to initiate the reboot process.")

    else:
        print("VM is powered off.")


def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        time.sleep(1)  # Bir süre bekleyerek döngüyü kontrol et
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(vm_name :str,vCenter_host_ip :str, vCenter_user :str, vCenter_password :str):
    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    vm_to_reboot = get_vm_by_name(content, vm_name)

    if vm_to_reboot is not None:
        reboot_vm(vm_to_reboot)
        
    else:
        print(f"VM with name {vm_name} not found")

    Disconnect(service_instance)
