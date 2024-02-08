from pyVim.connect import Disconnect
from ESXi.IaaS.ESXi_Connection.esxi_connection import *

def destroy_vm(vm):

    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        print(f"Shutting down VM -- {vm.name}...")
        task = vm.PowerOff()
        WaitForTask(task)

    task = vm.Destroy_Task()
    WaitForTask(task)

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(destroy_vm_name ,esxi_host_ip, esxi_user, esxi_password):

    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)
    vm_name_to_destroy = destroy_vm_name

    vm_to_destroy = get_vm_by_name(content, vm_name_to_destroy)

    if vm_to_destroy is not None:
        # Destroy the VM
        destroy_vm(vm_to_destroy)
    else:
        print(f"VM with name {vm_name_to_destroy} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
