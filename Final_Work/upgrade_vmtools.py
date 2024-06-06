from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import get_vm_by_name, create_vsphere_connection

def upgrade_vmtools(vCenterIP, username, password, vm_name):
    service_instance, content = create_vsphere_connection(vCenterIP, username, password)

    if service_instance is not None:
        vm_to_check = get_vm_by_name(content, vm_name)

        if vm_to_check is not None:
            vm_to_check.UpgradeTools_Task()
            print(f"VM Tools upgrade task initiated for VM {vm_name}")
        else:
            print(f"VM with name {vm_name} not found.")

        Disconnect(service_instance)


if __name__ == "__main__":
    esxi_host = "10.14.45.10"
    esxi_user = "administrator@vsphere.local"
    esxi_password = "Aa112233!"

    vm_name = "bülent_test_clone"

    upgrade_vmtools(esxi_host, esxi_user, esxi_password, vm_name)