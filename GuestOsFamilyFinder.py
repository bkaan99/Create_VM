from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def Find_GuestFullName(vm):
    guest_full_name = vm.config.guestFullName
    return guest_full_name

def Find_GuestFamily(guest_full_name):

    windows_keywords = [
        "Microsoft MS-DOS",
        "Microsoft Small Business Server 2003",
        "Microsoft Windows 10",
        "Microsoft Windows 2000",
        "Microsoft Windows 3.1",
        "Microsoft Windows 7",
        "Microsoft Windows 8",
        "Microsoft Windows 95",
        "Microsoft Windows 98",
        "Microsoft Windows NT",
        "Microsoft Windows Server 2003",
        "Microsoft Windows Server 2008",
        "Microsoft Windows Server 2012",
        "Microsoft Windows Server 2016",
        "Microsoft Windows Server 2019",
        "Microsoft Windows Server 2022",
        "Microsoft Windows Vista",
        "Microsoft Windows XP Professional"
    ]

    other_keywords = [
        "FreeBSD 11",
        "FreeBSD 12",
        "FreeBSD 13",
        "FreeBSD Pre-11",
        "IBM OS/2",
        "Novell NetWare 5.1",
        "Novell NetWare 6.x",
        "Oracle Solaris 10",
        "Oracle Solaris 11",
        "Other",
        "SCO OpenServer 5",
        "SCO OpenServer 6",
        "SCO UnixWare 7",
        "Serenity Systems eComStation 1",
        "Serenity Systems eComStation 2",
        "Sun Microsystems Solaris 8",
        "Sun Microsystems Solaris 9",
        "VMware ESX 4.x",
        "VMware ESXi 5.x",
        "VMware ESXi 6.0",
        "VMware ESXi 6.x",
        "VMware ESXi 7.0"
    ]

    macos_keywords = [
        "Apple Mac OS X 10.10",
        "Apple Mac OS X 10.11",
        "Apple Mac OS X 10.5",
        "Apple Mac OS X 10.6",
        "Apple Mac OS X 10.7",
        "Apple Mac OS X 10.8",
        "Apple Mac OS X 10.9",
        "Apple macOS 10.12",
        "Apple macOS 10.13",
        "Apple macOS 10.14",
        "Apple macOS 10.15",
        "Apple macOS 11",
        "Apple macOS 12"
    ]

    linux_keywords = [
        "Amazon Linux 2",
        "Amazon Linux 3",
        "Asianux 3",
        "Asianux 4",
        "Asianux 7",
        "CentOS 4/5",
        "CentOS 6",
        "CentOS 7",
        "CentOS 8",
        "CentOS 9",
        "CoreOS Linux",
        "Debian GNU/Linux 10",
        "Debian GNU/Linux 11",
        "Debian GNU/Linux 4",
        "Debian GNU/Linux 5",
        "Debian GNU/Linux 6",
        "Debian GNU/Linux 7",
        "Debian GNU/Linux 8",
        "Debian GNU/Linux 9",
        "MIRACLE LINUX 8",
        "Novell Open Enterprise Server",
        "Oracle Linux 4/5",
        "Oracle Linux 6",
        "Oracle Linux 7",
        "Oracle Linux 8",
        "Oracle Linux 9",
        "Other 2.4.x Linux",
        "Other 2.6.x Linux",
        "Other 3.x Linux",
        "Other 4.x Linux",
        "Other 5.x or later Linux",
        "Other Linux",
        "Red Hat Enterprise Linux 2.1",
        "Red Hat Enterprise Linux 3",
        "Red Hat Enterprise Linux 4",
        "Red Hat Enterprise Linux 5",
        "Red Hat Enterprise Linux 6",
        "Red Hat Enterprise Linux 7",
        "Red Hat Enterprise Linux 8",
        "Red Hat Enterprise Linux 9",
        "Red Hat Fedora",
        "SUSE Linux Enterprise 10",
        "SUSE Linux Enterprise 11",
        "SUSE Linux Enterprise 12",
        "SUSE Linux Enterprise 15",
        "SUSE Linux Enterprise 16",
        "SUSE Linux Enterprise 8/9",
        "SUSE openSUSE",
        "Ubuntu Linux",
        "VMware CRX Pod 1",
        "VMware Photon OS"
    ]

    all_keywords = windows_keywords + other_keywords + macos_keywords + linux_keywords

    for keyword in all_keywords:
        if keyword in guest_full_name:
            if keyword in windows_keywords:
                return "Windows"
            elif keyword in macos_keywords:
                return "Mac OS"
            elif keyword in linux_keywords:
                return "Linux"
            else:
                return "Other"

    return "Unknown Family"

def WaitForTask(task):
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Görev başarıyla tamamlandı.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Hata: {task.info.error}")
            task_done = True

def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    vm_name_to_reconfigure = "Clone-SUSE-Temp-15-3"

    vm_to_reconfigure = get_vm_by_name(content, vm_name_to_reconfigure)

    if vm_to_reconfigure is None:
        print(f"VM {vm_name_to_reconfigure} bulunamadı.")
        return

    guest_full_name = Find_GuestFullName(vm_to_reconfigure)

    guest_family = Find_GuestFamily(guest_full_name)

    Disconnect(service_instance)

    return guest_family

if __name__ == "__main__":
    main()
