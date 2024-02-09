from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def create_vsphere_connection(vCenterIP, username, password):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host=vCenterIP,
                                    user=username,
                                    pwd=password,
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()
    return service_instance, content

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def main(vCenterIP, username, password, vm_name):
    service_instance, content = create_vsphere_connection(vCenterIP, username, password)

    if service_instance is not None:
        vm_to_check = get_vm_by_name(content, vm_name)

        if vm_to_check is not None:
             if vm_to_check.guest.toolsStatus == vim.vm.GuestInfo.ToolsStatus.toolsOk:
                 CurrentState = True
                 return CurrentState

             else:
                CurrentState = False
                return CurrentState

        # Disconnect from vCenter
        Disconnect(service_instance)

