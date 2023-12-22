from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# ESXi host bilgileri
esxi_host = "10.14.45.11"
username = "root"
password = "Aa112233!"

def connect_to_vmware(esxi_host, username, password):
    """
    VMware ESXi host'a bağlanır ve bir ServiceInstance nesnesini döndürür.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE  # Sertifika doğrulamasını devre dışı bırak

    si = SmartConnect(host=esxi_host, user=username, pwd=password, port=443, sslContext=context)
    return si

def disconnect_from_vmware(si):
    """
    VMware ESXi host ile bağlantıyı kapatır.
    """
    Disconnect(si)

def list_vm_names_and_ids(esxi_host, username, password):
    """
    VMware ESXi host'tan mevcut tüm sanal makinelerin adlarını ve UUID'lerini listeler.
    """
    si = connect_to_vmware(esxi_host, username, password)

    # Sanal makineleri al
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view

    # Her bir sanal makinenin adını ve UUID'sini yazdır
    for vm in vms:
        vm_name = vm.summary.config.name
        vm_uuid = vm.summary.config.instanceUuid
        print(f"VM Adı: {vm_name}")
        print(f"VM UUID: {vm_uuid}")
        print("-" * 30)

    disconnect_from_vmware(si)

def get_vm_info_by_id(vm_id, esxi_host, username, password):
    """
    Belirli bir VM ID'sine sahip VMware ESXi host'tan sanal makine bilgilerini çeker ve yazdırır.
    """
    si = connect_to_vmware(esxi_host, username, password)

    # Sanal makineleri al
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view

    # Belirli VM ID'sine sahip olanı bul
    vm = None
    for virtual_machine in vms:
        if virtual_machine.summary.config.instanceUuid == vm_id:
            vm = virtual_machine
            break

    # Belirli VM ID'sine sahip bir VM bulunamazsa hata mesajı ver
    if not vm:
        print(f"VM ID'si {vm_id} olan bir sanal makine bulunamadı.")
        disconnect_from_vmware(si)
        return

    # Sanal makine bilgilerini yazdır
    print(f"VM Adı: {vm.summary.config.name}")
    print(f"VM UUID: {vm.summary.config.instanceUuid}")
    print(f"VM Durumu: {vm.summary.runtime.powerState}")
    print(f"VM İşletim Sistemi: {vm.summary.config.guestFullName}")

    get_capabilities(vm)

    disconnect_from_vmware(si)

def get_vm_info_all(esxi_host, username, password):
    """
    VMware ESXi host'tan mevcut tüm sanal makinelerin bilgilerini çeker ve yazdırır.
    """

    si = connect_to_vmware(esxi_host, username, password)
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view

    for vm in vms:
        get_vm_config(vm)

    disconnect_from_vmware(si)

def get_capabilities(vm):
    capabilities = {
        "bootOptionsSupported": vm.capability.bootOptionsSupported,
        "bootRetryOptionsSupported": vm.capability.bootRetryOptionsSupported,
        "changeModeDisksSupported": vm.capability.changeModeDisksSupported,
        "changeTrackingSupported": vm.capability.changeTrackingSupported,
        "consolePreferencesSupported": vm.capability.consolePreferencesSupported,
        "cpuFeatureMaskSupported": vm.capability.cpuFeatureMaskSupported,
        "disableSnapshotsSupported": vm.capability.disableSnapshotsSupported,
        "diskOnlySnapshotOnSuspendedVMSupported": vm.capability.diskOnlySnapshotOnSuspendedVMSupported,
        "diskSharesSupported": vm.capability.diskSharesSupported,
        "dynamicProperty": vm.capability.dynamicProperty,
        "dynamicType": vm.capability.dynamicType,
        "featureRequirementSupported": vm.capability.featureRequirementSupported,
        "guestAutoLockSupported": vm.capability.guestAutoLockSupported,
        "hostBasedReplicationSupported": vm.capability.hostBasedReplicationSupported,
        "lockSnapshotsSupported": vm.capability.lockSnapshotsSupported,
        "memoryReservationLockSupported": vm.capability.memoryReservationLockSupported,
        "memorySnapshotsSupported": vm.capability.memorySnapshotsSupported,
        "multipleCoresPerSocketSupported": vm.capability.multipleCoresPerSocketSupported,
        "multipleSnapshotsSupported": vm.capability.multipleSnapshotsSupported,
        "nestedHVSupported": vm.capability.nestedHVSupported,
        "npivWwnOnNonRdmVmSupported": vm.capability.npivWwnOnNonRdmVmSupported,
        "perVmEvcSupported": vm.capability.perVmEvcSupported,
        "pmemFailoverSupported": vm.capability.pmemFailoverSupported,
        "poweredOffSnapshotsSupported": vm.capability.poweredOffSnapshotsSupported,
        "poweredOnMonitorTypeChangeSupported": vm.capability.poweredOnMonitorTypeChangeSupported,
        "quiescedSnapshotsSupported": vm.capability.quiescedSnapshotsSupported,
        "recordReplaySupported": vm.capability.recordReplaySupported,
        "requireSgxAttestationSupported": vm.capability.requireSgxAttestationSupported,
        "revertToSnapshotSupported": vm.capability.revertToSnapshotSupported,
        "s1AcpiManagementSupported": vm.capability.s1AcpiManagementSupported,
        "seSparseDiskSupported": vm.capability.seSparseDiskSupported,
        "secureBootSupported": vm.capability.secureBootSupported,
        "settingDisplayTopologySupported": vm.capability.settingDisplayTopologySupported,
        "settingScreenResolutionSupported": vm.capability.settingScreenResolutionSupported,
        "settingVideoRamSizeSupported": vm.capability.settingVideoRamSizeSupported,
        "sevSupported": vm.capability.sevSupported,
        "snapshotConfigSupported": vm.capability.snapshotConfigSupported,
        "snapshotOperationsSupported": vm.capability.snapshotOperationsSupported,
        "suspendToMemorySupported": vm.capability.suspendToMemorySupported,
        "swapPlacementSupported": vm.capability.swapPlacementSupported,
        "toolsAutoUpdateSupported": vm.capability.toolsAutoUpdateSupported,
        "toolsSyncTimeAllowSupported": vm.capability.toolsSyncTimeAllowSupported,
        "toolsSyncTimeSupported": vm.capability.toolsSyncTimeSupported,
        "vPMCSupported": vm.capability.vPMCSupported,
        "vendorDeviceGroupSupported": vm.capability.vendorDeviceGroupSupported,
        "virtualExecUsageIgnored": vm.capability.virtualExecUsageIgnored,
        "virtualMmuUsageIgnored": vm.capability.virtualMmuUsageIgnored,
        "virtualMmuUsageSupported": vm.capability.virtualMmuUsageSupported,
        "vmNpivWwnDisableSupported": vm.capability.vmNpivWwnDisableSupported,
        "vmNpivWwnSupported": vm.capability.vmNpivWwnSupported,
        "vmNpivWwnUpdateSupported": vm.capability.vmNpivWwnUpdateSupported,
    }

    print("Capabilities:")
    for key, value in capabilities.items():
        print(f"    {key}: {value}")
    print("-" * 30)

    #return capabilities

def get_vm_config(vm):
    config_dict = {
        "alternateGuestName": vm.config.alternateGuestName,
        "annotation": vm.config.annotation,
        "bootOptions": {
            "dynamicType": vm.config.bootOptions.dynamicType,
            "dynamicProperty": vm.config.bootOptions.dynamicProperty,
            "bootDelay": vm.config.bootOptions.bootDelay,
            "enterBIOSSetup": vm.config.bootOptions.enterBIOSSetup,
            "efiSecureBootEnabled": vm.config.bootOptions.efiSecureBootEnabled,
            "bootRetryEnabled": vm.config.bootOptions.bootRetryEnabled,
            "bootRetryDelay": vm.config.bootOptions.bootRetryDelay,
            "bootOrder": vm.config.bootOptions.bootOrder,
            "networkBootProtocol": vm.config.bootOptions.networkBootProtocol
        },
        "changeTrackingEnabled": vm.config.changeTrackingEnabled,
        "changeVersion": vm.config.changeVersion,
        "consolePreferences": vm.config.consolePreferences,
        "contentLibItemInfo": vm.config.contentLibItemInfo,
        "cpuAffinity": vm.config.cpuAffinity,
        "cpuAllocation": {
            "dynamicType": vm.config.cpuAllocation.dynamicType,
            "dynamicProperty": vm.config.cpuAllocation.dynamicProperty,
            "reservation": vm.config.cpuAllocation.reservation,
            "expandableReservation": vm.config.cpuAllocation.expandableReservation,
            "limit": vm.config.cpuAllocation.limit,
            "shares": {
                "dynamicType": vm.config.cpuAllocation.shares.dynamicType,
                "dynamicProperty": vm.config.cpuAllocation.shares.dynamicProperty,
                "shares": vm.config.cpuAllocation.shares.shares,
                "level": vm.config.cpuAllocation.shares.level
            },
            "overheadLimit": vm.config.cpuAllocation.overheadLimit
        },
        "cpuFeatureMask": vm.config.cpuFeatureMask,
        "cpuHotAddEnabled": vm.config.cpuHotAddEnabled,
        "cpuHotRemoveEnabled": vm.config.cpuHotRemoveEnabled,
        "createDate": vm.config.createDate,
        "datastoreUrl": [{
            "name": item.name,
            "url": item.url
        } for item in vm.config.datastoreUrl],
        # ... (diğer alanları ekleyin)
    }

    print("Config:")
    for key, value in config_dict.items():
        print(f"    {key}: {value}")
    print("-" * 30)


    return config_dict



#list_vm_names_and_ids("10.14.45.11", "root", "Aa112233!")
#get_vm_info_by_id("52fcb522-4260-6635-e2dd-0f687cf79f0a", esxi_host, username, password)
get_vm_info_all(esxi_host, username, password)
