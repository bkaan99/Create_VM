from pyVim.connect import Disconnect
from ESXi.IaaS.ESXi_Connection.esxi_connection import *
from pyVmomi import vim

def get_vm_by_name(content, vm_name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for child in container.view:
        if child.name == vm_name:
            return child
    return None

def power_on_vm(vm):
    if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
        task = vm.PowerOnVM_Task()
        WaitForTask(task)
    else:
        print("VM is already powered on.")

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(vm_name_to_power_on, esxi_host_ip, esxi_user, esxi_password):
    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)
    vm_to_power_on = get_vm_by_name(content, vm_name_to_power_on)

    if vm_to_power_on is not None:
        power_on_vm(vm_to_power_on)
    else:
        print(f"VM with name {vm_name_to_power_on} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
