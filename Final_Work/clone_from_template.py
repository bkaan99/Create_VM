from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def clone_template(si, template_name, clone_name):
    content = si.RetrieveContent()
    vm_folder = content.rootFolder.childEntity[0].vmFolder
    template = get_template_by_name(content, template_name)

    clone_spec = create_clone_spec(content, template, vm_folder, clone_name)
    clone_task = template.CloneVM_Task(folder=vm_folder, name=clone_name, spec=clone_spec)

    print("Cloning template. This may take a while...")
    while clone_task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        continue

    if clone_task.info.state == vim.TaskInfo.State.success:
        print("Template cloned successfully.")
    else:
        print("Error cloning template:", clone_task.info.error.msg)

def get_template_by_name(content, template_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.config.template and vm.name == template_name:
            return vm
    return None

def create_clone_spec(content, template, folder, clone_name):
    clone_spec = vim.vm.CloneSpec()
    relocate_spec = vim.vm.RelocateSpec()
    relocate_spec.folder = folder
    # Here, you should provide a valid ResourcePool object
    resource_pool = get_resource_pool(content)
    relocate_spec.pool = resource_pool
    clone_spec.location = relocate_spec
    clone_spec.powerOn = False

    clone_spec.config = vim.vm.ConfigSpec()
    clone_spec.config.name = clone_name

    return clone_spec

def get_resource_pool(content):
    resource_pool = None
    cluster = get_cluster(content)
    if cluster:
        rp = cluster.resourcePool
        resource_pool = rp
    return resource_pool

def get_cluster(content):
    cluster = None
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.ClusterComputeResource], True)
    for c in container.view:
        # first cluster in the list
        cluster = c
        break
    return cluster

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
        # Call clone_template function with desired template name and clone name
        clone_template(si, "bkaan_deneme_clone", "clone_name_here")
    except Exception as e:
        print("Error:", e)

    # Disconnect from vSphere server
    Disconnect(si)

if __name__ == "__main__":
    main()
