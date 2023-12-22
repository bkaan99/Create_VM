from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def get_datacenter_for_vm(vm):
    # Traverse up the object hierarchy to find the associated Datacenter
    obj = vm
    while obj and not isinstance(obj, vim.Datacenter):
        obj = obj.parent
    return obj

def register_vmx_file(datacenter, content, vmx_file_path):
    try:


        for child in content.rootFolder.childEntity:
            if isinstance(child, vim.Datacenter):
                datacenter = child
                break

        if datacenter is None:
            print("Datacenter bulunamadı.")
            return None


        # Get the VM folder
        vm_folder = datacenter.vmFolder

        # Create a new VM config spec
        vm_config_spec = vim.vm.ConfigSpec()

        # Set the VMX file path
        vm_file_info = vim.vm.FileInfo(logDirectory=None, snapshotDirectory=None, suspendDirectory=None, vmPathName=vmx_file_path)
        vm_config_spec.files = vm_file_info
        resource_pool = datacenter.hostFolder.childEntity[0].resourcePool
        vm_config_spec.name = "bkaan_deneme"
        # Create a new VM
        vm = vm_folder.CreateVM_Task(config=vm_config_spec, pool=resource_pool)
        WaitForTask(vm)

        print(f"VMX file registered successfully: {vmx_file_path}")

    except Exception as e:
        print(f"Error: {e}")

def WaitForTask(task):
    """Waits and provides updates on a vSphere task until it is completed."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Task completed successfully.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Error: {task.info.error}")
            task_done = True

def main():
    vcenter_server = "10.14.45.11"
    vcenter_user = "root"
    vcenter_password = "Aa112233!"
    vm_name_to_rename = "bkaan_deneme"
    new_vm_name = vm_name_to_rename + "/bkaan_deneme.vmx"

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

    # Retrieve the VM to register
    content = si.RetrieveContent()
    vm_to_register = get_vm_by_name(content, vm_name_to_rename)

    if vm_to_register is not None:
        # Get the datastore name
        datastore_name = vm_to_register.datastore[0].info.name

        # Get the VMX file path
        vmx_file_path = f"[{datastore_name}] {new_vm_name}"

        # Get the parent datacenter
        datacenter = get_datacenter_for_vm(vm_to_register)

        if datacenter is not None:
            # Register the VMX file
            register_vmx_file(datacenter, content, vmx_file_path)
        else:
            print(f"Datacenter not found for VM: {vm_name_to_rename}")
    else:
        print(f"VM with name {vm_name_to_rename} not found")

    # Disconnect from vCenter
    Disconnect(si)

if __name__ == "__main__":
    main()
