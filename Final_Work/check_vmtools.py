from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def create_vsphere_connection():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()
    return service_instance, content

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def get_vm_tools_status(vm):
    result = {}

    if vm.guest is not None:
        tools_status = vm.guest.toolsStatus
        result["tools_status_info"] = ""

        if tools_status == "toolsNotInstalled":
            result["tools_status_info"] = "VMware Tools yüklü değil."

        elif tools_status == "toolsNotRunning":
            result["tools_status_info"] = "VMware Tools yüklü, ancak çalışmıyor."

        elif tools_status == "toolsOk":
            result["tools_status_info"] = "VMware Tools yüklü ve çalışıyor."

        elif tools_status == "toolsOld":
            result["tools_status_info"] = "VMware Tools yüklü, ancak güncel değil."

        tools_running_status = vm.guest.toolsRunningStatus
        result["tools_running_status_info"] = "Unknown"

        if tools_running_status == "guestToolsRunning":
            result["tools_running_status_info"] = "VMware Tools çalışıyor."

        elif tools_running_status == "guestToolsNotRunning":
            #check vm power state
            if vm.runtime.powerState == "poweredOff":
                result["tools_running_status_info"] = "VMware Tools çalışmıyor. VM kapalı durumda."
            elif vm.runtime.powerState == "poweredOn":
                result["tools_running_status_info"] = "VMware Tools çalışmıyor. VM açık durumda."

        elif tools_running_status == "guestToolsExecutingScripts":
            result["tools_running_status_info"] = "VMware Tools script çalıştırıyor."

    else:
        result["tools_status_info"] = "VMware Tools status not available"
        result["tools_running_status_info"] = "VMware Tools running status not available"

    return result

def main(vm_name):
    service_instance, content = create_vsphere_connection()

    if service_instance is not None:
        vm_to_check = get_vm_by_name(content, vm_name)

        if vm_to_check is not None:
            result = get_vm_tools_status(vm_to_check)
            print(f"VMware Tools status for VM '{vm_name}': ---> {result['tools_status_info']}")
            print(f"VMware Tools running status for VM '{vm_name}': ---> {result['tools_running_status_info']}")
        else:
            print(f"VM with name {vm_name} not found")

        # Disconnect from vCenter
        Disconnect(service_instance)

if __name__ == "__main__":
    vm_name_to_check = "Clone-SUSE-Temp-15-3"  # Replace with the name of the VM you want to check
    main(vm_name_to_check)