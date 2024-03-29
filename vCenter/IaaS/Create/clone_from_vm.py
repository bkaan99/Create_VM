from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
from pyVmomi import vim

def clone_vm(si, vm_name, clone_name):
    content = si.RetrieveContent()
    vm_folder = content.rootFolder.childEntity[0].vmFolder
    vm = get_vm_by_name(content, vm_name)

    template = vm.CloneVM_Task(folder=vm_folder, name=clone_name, spec=create_clone_spec(vm))
    print("Cloning VM. This may take a while...")
    while template.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        continue

    if template.info.state == vim.TaskInfo.State.success:
        print("VM cloned successfully.")
    else:
        print("Error cloning VM:", template.info.error.msg)


def create_clone_spec(vm):
    clone_spec = vim.vm.CloneSpec()
    clone_spec.location = vim.vm.RelocateSpec()

    clone_spec.config = vim.vm.ConfigSpec()
    clone_spec.config.numCPUs = vm.config.hardware.numCPU
    clone_spec.config.memoryMB = vm.config.hardware.memoryMB

    return clone_spec


def main(vCenter_host_ip, vCenter_user, vCenter_password, vm_name, clone_name):

    service_instance, content = create_vsphere_connection(host=vCenter_host_ip, user=vCenter_user, password=vCenter_password)

    if not service_instance:
        print("Failed to connect to vSphere server.")
        return

    try:
        # Call clone_vm function with desired VM name and clone name
        clone_vm(service_instance, vm_name= vm_name, clone_name= clone_name)
    except Exception as e:
        print("Error:", e)

    # Disconnect from vSphere server
    Disconnect(service_instance)


if __name__ == "__main__":
    main()
