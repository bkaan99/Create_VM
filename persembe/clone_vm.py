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

def get_resource_pool(content, pool_name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.ResourcePool], True
    )
    for child in container.view:
        if child.name == pool_name:
            return child
    return None

def get_folder(content, folder_name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.Folder], True
    )
    for child in container.view:
        if child.name == folder_name:
            return child
        else:
            return None

def clone_vm(si, vm, clone_name, vm_folder=None, datastore_name=None, datastorecluster_name=None,
             cluster_name=None, resource_pool=None, power_on=False, opaque_network_name=None):
    relocate_spec = vim.vm.RelocateSpec()

    if resource_pool:
        relocate_spec.pool = get_resource_pool(si.content, resource_pool)

    clone_spec = vim.vm.CloneSpec(
        location=relocate_spec,
        powerOn=power_on,
        template=False,
        customization=None
    )

    try:
        # Folder'ı uygun bir vim.Folder nesnesine dönüştür
        folder = get_folder(si.content, vm_folder)

        # Clone işlemini gerçekleştirin ve hedef dizini belirtin
        clone_task = vm.Clone(name=clone_name, folder=folder, spec=clone_spec)
        WaitForTask(clone_task)
    except Exception as e:
        print(f"Klon işlemi sırasında hata oluştu: {e}")
        if hasattr(e, 'msg'):
            print(f"Hata detayları: {e.msg}")

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Görev başarıyla tamamlandı")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Görev sırasında hata oluştu: %s" % task.info.error)

def main():
    vcenter_server = "10.14.45.11"
    vcenter_user = "root"
    vcenter_password = "Aa112233!"
    vm_name_to_clone = "bkaan_deneme"
    clone_name = "deneme_clone"
    vm_folder = "MyVMFolder"  # Değiştirilmesi gereken dizin adını ekleyin

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

    # Retrieve the VM to clone
    content = si.RetrieveContent()
    vm_to_clone = get_vm_by_name(content, vm_name_to_clone)

    if vm_to_clone is not None:
        # Clone the VM
        clone_vm(si, vm_to_clone, clone_name, vm_folder=vm_folder, datastore_name='MyDatastore', power_on=True)
    else:
        print(f"{vm_name_to_clone} adlı VM bulunamadı")

    # Disconnect from vCenter
    Disconnect(si)

if __name__ == "__main__":
    main()
