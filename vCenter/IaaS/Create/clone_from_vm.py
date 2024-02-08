from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

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

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def create_clone_spec(vm):
    clone_spec = vim.vm.CloneSpec()
    clone_spec.location = vim.vm.RelocateSpec()

    clone_spec.config = vim.vm.ConfigSpec()
    clone_spec.config.numCPUs = vm.config.hardware.numCPU
    clone_spec.config.memoryMB = vm.config.hardware.memoryMB

    return clone_spec


def main():
    # vSphere server credentials
    esxi_host_ip = "10.14.45.10"
    esxi_user = "administrator@vsphere.local"
    esxi_password = "Aa112233!"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Connect to vSphere server
    si = SmartConnect(host=esxi_host_ip, user=esxi_user, pwd=esxi_password, sslContext=ssl_context)

    if not si:
        print("Failed to connect to vSphere server.")
        return

    try:
        # Call clone_vm function with desired VM name and clone name
        clone_vm(si, "bkaan_deneme", "bkaan_deneme_clone")
    except Exception as e:
        print("Error:", e)

    # Disconnect from vSphere server
    Disconnect(si)


if __name__ == "__main__":
    main()
