# vsphere_connection.py
from pyVim import connect
import ssl
from pyVmomi import vim


def create_vsphere_connection(host, user, password):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = connect.SmartConnect(host=host,
                                            user=user,
                                            pwd=password,
                                            sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    return service_instance , content

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None
