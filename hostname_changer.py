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

def rename_vm(vm, new_name):
    spec = vim.vm.ConfigSpec()
    spec.name = new_name
    task = vm.ReconfigVM_Task(spec=spec)
    WaitForTask(task)


def customize_vm_hostname(vm, new_hostname):
    # Create a customization specification
    customization_spec = vim.vm.customization.Specification()
    customization_spec.identity = vim.vm.customization.LinuxPrep(
        hostname=vim.vm.customization.FixedName(name=new_hostname))

    # Customize the VM
    spec = vim.vm.ConfigSpec()
    spec.customization = customization_spec
    task = vm.ReconfigVM_Task(spec=spec)
    WaitForTask(task)

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)

def main():
    vcenter_server = "10.14.45.11"
    vcenter_user = "root"
    vcenter_password = "Aa112233!"
    vm_name_to_rename = "11"
    new_vm_name = "11"

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

    # Retrieve the VM to rename
    content = si.RetrieveContent()
    vm_to_rename = get_vm_by_name(content, vm_name_to_rename)

    if vm_to_rename is not None:
        # Rename the VM
        rename_vm(vm_to_rename, new_vm_name)

        # Change the VM's hostname
        customize_vm_hostname(vm_to_rename, new_vm_name)
    else:
        print(f"VM with name {vm_name_to_rename} not found")

    # Disconnect from vCenter
    Disconnect(si)

if __name__ == "__main__":
    main()
