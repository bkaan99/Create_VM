from pyVim.connect import Disconnect
from ESXi.IaaS.ESXi_Connection.esxi_connection import *

def find_first_vm(content):
    for child in content.rootFolder.childEntity:
        if isinstance(child, vim.Datacenter):
            datacenter = child
            vm_folder = datacenter.vmFolder
            view = content.viewManager.CreateContainerView(datacenter, [vim.VirtualMachine], True)
            vms = view.view
            view.Destroy()
            if vms:
                return vms[0]
    return None

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

def find_file_in_folder(ds ,target_folder):
    search = vim.HostDatastoreBrowserSearchSpec()
    search.matchPattern = "*.vmx"
    search_ds = ds.browser.SearchDatastoreSubFolders_Task(datastorePath="[%s]" % ds.name, searchSpec=search)
    while search_ds.info.state != "success":
        #print(search_ds.info.state)
        #print(search_ds.info.error.msg)
        pass
    results = search_ds.info.result

    for result in results:
        # Adjust the comparison to consider the datastore name in the folderPath
        if f"[{ds.name}] {target_folder}" in result.folderPath:
            print("Found Folder on:", result.folderPath)
            for f in result.file:
                if f.path.endswith(".vmx"):
                    print("Found file:", f.path)
                    return f.path

    print("File not found.")
    return None

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


def main(register_vm_name, esxi_host_ip, esxi_user, esxi_password , copied_folder_name):

    service_instance, content = create_vsphere_connection( esxi_host_ip, esxi_user, esxi_password)

    source_vm = find_first_vm(content)

    if source_vm is None:
        print(f"VM {source_vm.name} not found.")
        return

    #Burada kodda güncellme yapılacak datastore kısmı 0. al diyorum böyle bir şey ilerde hata verdirebilir.
    datastore = source_vm.datastore[0]

    folder_name = copied_folder_name

    file_name = find_file_in_folder(datastore, folder_name)

    source_file_path = f"[{datastore.name}] {folder_name}/{file_name}"

    register_vmx_file(datastore, content, source_file_path, register_vm_name)

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
