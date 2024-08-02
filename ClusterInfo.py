import os
import ssl
from RabbitMQ.rabbitmq_helper import MessageHandler, Config, RabbitMQConnection, ScriptListener

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def get_all_resource_pools(content):
    resource_pool_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.ResourcePool], True)
    resource_pools = resource_pool_view.view
    resource_pool_view.Destroy()
    return resource_pools


def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    ScriptListener.script_listener(os.path.basename(__file__), status='running')

    resource_pools = get_all_resource_pools(content)
    print("Tüm kaynak havuzları:")
    for resource_pool in resource_pools:
        print(resource_pool.name)

    Disconnect(service_instance)


if __name__ == "__main__":
    main()
    ScriptListener.script_listener(os.path.basename(__file__), status='finished')