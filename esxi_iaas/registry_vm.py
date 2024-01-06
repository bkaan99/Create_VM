from pyVim.connect import SmartConnect, Disconnect
from pyVim import connect
from pyVmomi import vim
from esxi_connection import *

import ssl

def register_vmx_file(datacenter, content, vmx_file_path, RegisterVm_name):
    try:

        for child in content.rootFolder.childEntity:
            if isinstance(child, vim.Datacenter):
                datacenter = child
                break

        if datacenter is None:
            print("Datacenter bulunamadı.")
            return None

        pool = datacenter.hostFolder.childEntity[0].resourcePool

        # Get the VM folder
        vm_folder = datacenter.vmFolder

        vm = vm_folder.RegisterVm(path=vmx_file_path,name=RegisterVm_name, asTemplate=False, pool=pool)
        WaitForTask(vm)

        print(f"VMX file registered successfully: {vmx_file_path}")

        print("VM created: %s" , RegisterVm_name)

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


def main(register_vm_name, copied_vm_name):

    service_instance, content = create_vsphere_connection("10.14.45.11", "root", "Aa112233!")

    source_vm_name = copied_vm_name

    source_vm = get_vm_by_name(content, source_vm_name)

    if source_vm is None:
        print(f"VM {source_vm_name} not found.")
        return

    datastore = source_vm.datastore[0]

    folder_name = "cuma_mesai"

    file_name = "bkaan_centos"

    source_file_path = f"[{datastore.name}] {folder_name}/{file_name}.vmx"

    register_vmx_file(datastore, content, source_file_path, register_vm_name)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
