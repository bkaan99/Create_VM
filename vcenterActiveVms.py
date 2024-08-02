from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
from vCenter.IaaS.Connections import db_connection


def get_vm_by_name(content, vm_name):
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for child in container.view:
        if child.name == vm_name:
            return child
    return None

def WaitForTask(task):
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        pass
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully")
    elif task.info.state == vim.TaskInfo.State.error:
        print("Error during task execution: %s" % task.info.error)


def get_vm_power_state(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        return "poweredOn"
    elif vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        return "poweredOff"
    else:
        return "unknown"

def get_all_vms_with_power_state(content):
    vm_list = []
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for vm in container.view:
        vm_info = {
            "name": vm.name,
            "power_state": get_vm_power_state(vm)
        }
        vm_list.append(vm_info)
    return vm_list

def main():
    # vSphere server credentials
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    # Disable SSL certificate verification
    sslContext = ssl.create_default_context()
    sslContext.check_hostname = False
    sslContext.verify_mode = ssl.CERT_NONE

    # Connect to vCenter
    si = SmartConnect(
        host=vCenter_host_ip,
        user=vCenter_user,
        pwd=vCenter_password,
        sslContext=sslContext,
    )

    content = si.RetrieveContent()
    all_vms = get_all_vms_with_power_state(content)

    connect_Postgres, cursorForPostgres = db_connection.connect_Postgres()

    sql_list = []

    for vm_info in all_vms:
        try:
            name = vm_info["name"]
            power_state = vm_info["power_state"]
            onlineOfflineStatus = "true" if power_state == "poweredOn" else "false"

            # SQL sorgusunu oluştur
            sql = "update kr_vm_list set onlineofflinestatus = 'true' where vmName = 'BkaanGurgen'"
            # SQL sorgusunu çalıştırmak yerine sorgu ve değerleri bir listeye ekle
            sql_list.append((sql, (onlineOfflineStatus, name)))
            print(f"VM Name: {name}, Power State: {power_state}")
        except Exception as e:
            print(e)

    # Tüm SQL sorgularını çalıştır
    for sql, val in sql_list:
        cursorForPostgres.execute(sql, val)
    # Disconnect from vCenter
    Disconnect(si)

if __name__ == "__main__":
    main()
