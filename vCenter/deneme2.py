from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

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

def main():
    vcenter_server = "10.14.45.10"
    vcenter_user = "administrator@vsphere.local"
    vcenter_password = "Aa112233!"
    vm_name_to_power_on = "bkaan_deneme"

    # Disable SSL certificate verification
    sslContext = ssl.create_default_context()
    sslContext.check_hostname = False
    sslContext.verify_mode = ssl.CERT_NONE

    # Connect to vCenter
    si = SmartConnect(
        host=vcenter_server,
        user=vcenter_user,
        pwd=vcenter_password,
        sslContext=sslContext,
    )

    # Retrieve the VM to power on
    content = si.RetrieveContent()
    vm_to_power_on = get_vm_by_name(content, vm_name_to_power_on)

    if vm_to_power_on is not None:
        # Power on the VM
        power_on_vm(vm_to_power_on)
    else:
        print(f"VM with name {vm_name_to_power_on} not found")

    # Disconnect from vCenter
    Disconnect(si)

if __name__ == "__main__":
    main()
