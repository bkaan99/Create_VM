from pyVim.connect import SmartConnect, Disconnect
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

def power_off_vm(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        task = vm.PowerOffVM_Task()
        wait_for_task(task)
        print("VM powered off.")
    else:
        print("VM is already powered off.")

def wait_for_task(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main(power_on_vm, esxi_host_ip, esxi_user, esxi_password):
    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)
    vm_to_manage = get_vm_by_name(content, power_on_vm)

    if vm_to_manage is not None:
        # Power off the VM if it's powered on
        power_off_vm(vm_to_manage)
    else:
        print(f"VM with name {power_on_vm} not found")

    # Disconnect from vCenter
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
