# vsphere_connection.py
import sys
from pyVim import connect
import ssl
from pyVmomi import vim
import socket


def create_vsphere_connection(host, user, password, timeout=10):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        socket.create_connection((host, 443), timeout=timeout)
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=password,
                                                sslContext=ssl_context)

    except (ssl.SSLError, socket.timeout, socket.error) as e:
        print(f"Bağlantı Hatası: {e}")
        # exit close the program
        sys.exit(1)

    content = service_instance.RetrieveContent()

    return service_instance , content

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None
