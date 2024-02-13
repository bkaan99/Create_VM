from pyVim.connect import Disconnect
from vCenter.IaaS.Connections.vSphere_connection import *

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

