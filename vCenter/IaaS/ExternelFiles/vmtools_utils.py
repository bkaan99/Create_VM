from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import get_vm_by_name, create_vsphere_connection
from pyVmomi import vim

def upgrade_vmtools(vm_to_check):
    if vm_to_check is not None:
        vm_to_check.UpgradeTools_Task()
        print("VM Tools upgrade task initiated for VM .")
    else:
        print("VM with name  not found.")

    Disconnect(service_instance)

def config_vmtools(vm_to_check):
    vm_config_spec = vim.vm.ConfigSpec()
    vm_config_spec.tools = vim.vm.ToolsConfigInfo()
    vm_config_spec.tools.toolsUpgradePolicy = "upgradeAtPowerCycle"
    vm_to_check.ReconfigVM_Task(vm_config_spec)

def vmtool_status(vCenterIP, username, password, vm_name):
    service_instance, content = create_vsphere_connection(vCenterIP, username, password)
    vm_to_check = get_vm_by_name(content, vm_name)

    if (
        vm_to_check is not None
        and vm_to_check.guest.toolsStatus == vim.vm.GuestInfo.ToolsStatus.toolsOk
    ):
        CurrentState = True
        return CurrentState

    else:
        CurrentState = False
        return CurrentState


if __name__ == "__main__":

    vCenterIP = "10.14.45.10"
    username = "administrator@vsphere.local"
    password = "Aa112233!"

    vm_name = "bülent_test_clone"

    service_instance, content = create_vsphere_connection(vCenterIP, username, password)

    if service_instance is not None:
        vm_to_check = get_vm_by_name(content, vm_name)

        upgrade_vmtools(vm_to_check)

        config_vmtools(vm_to_check)
        print("")