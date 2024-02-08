from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *
from pyVmomi import vim

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
        print("Template cloned successfully as", clone_name)
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
        cluster = c
        break
    return cluster

def main(vCenter_host_ip, vCenter_user, vCenter_password, template_name, clone_name):

    service_instance, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    if not service_instance:
        print("Failed to connect to vSphere server.")
        return

    try:
        # Call clone_template function with desired template name and clone name
        clone_template(service_instance, template_name= template_name, clone_name= clone_name)
    except Exception as e:
        print("Error:", e)

    # Disconnect from vSphere server
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
