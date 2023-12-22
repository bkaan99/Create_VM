from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def connect_to_vmware(esxi_host, username, password):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=esxi_host, user=username, pwd=password, port=443, sslContext=context)
    return si

def disconnect_from_vmware(si):
    Disconnect(si)

def list_vm_names_and_ids(si):
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view

    print("Sanal Makineler:")
    for vm in vms:
        vm_name = vm.summary.config.name
        vm_uuid = vm.summary.config.instanceUuid
        print(f"VM Adı: {vm_name}")
        print(f"VM UUID: {vm_uuid}")
        print("-" * 30)

def get_vm_info_by_id(si, vm_id):
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view

    vm_found = False
    for virtual_machine in vms:
        if virtual_machine.summary.config.instanceUuid == vm_id:
            vm_found = True
            print(f"VM Adı: {virtual_machine.summary.config.name}")
            print(f"VM UUID: {virtual_machine.summary.config.instanceUuid}")
            print(f"VM Durumu: {virtual_machine.summary.runtime.powerState}")
            print(f"VM İşletim Sistemi: {virtual_machine.summary.config.guestFullName}")
            print("-" * 30)
            get_vm_config(virtual_machine)

    if not vm_found:
        print(f"VM ID'si {vm_id} olan bir sanal makine bulunamadı.")

def get_vm_info_all(si):
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view

    for vm in vms:
        print(f"VM Adı: {vm.summary.config.name}")
        print(f"VM UUID: {vm.summary.config.instanceUuid}")
        get_capability(vm)

def get_capability(vm):
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
            "reservation": vm.config.cpuAllocation.reservation,
            "expandableReservation": vm.config.cpuAllocation.expandableReservation,
            "limit": vm.config.cpuAllocation.limit,
            "shares": {
                "shares": vm.config.cpuAllocation.shares.shares,
                "level": vm.config.cpuAllocation.shares.level
            },
            "overheadLimit": vm.config.cpuAllocation.overheadLimit
        },
        "cpuFeatureMask": [
            {
                "level": item.level,
                "vendor": item.vendor,
                "eax": item.eax,
                "ebx": item.ebx,
                "ecx": item.ecx,
                "edx": item.edx
            } for item in vm.config.cpuFeatureMask
        ],
        "cpuHotAddEnabled": vm.config.cpuHotAddEnabled,
        "cpuHotRemoveEnabled": vm.config.cpuHotRemoveEnabled,
        "createDate": vm.config.createDate,
        "datastoreUrl": [
            {
                "name": item.name,
                "url": item.url
            } for item in vm.config.datastoreUrl
        ],
        "defaultPowerOps": {
            "powerOffType": vm.config.defaultPowerOps.powerOffType,
            "suspendType": vm.config.defaultPowerOps.suspendType,
            "resetType": vm.config.defaultPowerOps.resetType,
            "defaultPowerOffType": vm.config.defaultPowerOps.defaultPowerOffType,
            "defaultSuspendType": vm.config.defaultPowerOps.defaultSuspendType,
            "defaultResetType": vm.config.defaultPowerOps.defaultResetType,
            "standbyAction": vm.config.defaultPowerOps.standbyAction
        },
        "deviceGroups": vm.config.deviceGroups,
        "deviceSwap": vm.config.deviceSwap,
        "extraConfig": [
            {
                "key": item.key,
                "value": item.value
            } for item in vm.config.extraConfig
        ],
        "files": {
            "vmPathName": vm.config.files.vmPathName,
            "snapshotDirectory": vm.config.files.snapshotDirectory,
            "suspendDirectory": vm.config.files.suspendDirectory,
            "logDirectory": vm.config.files.logDirectory,
            "ftMetadataDirectory": vm.config.files.ftMetadataDirectory
        },
        "firmware": vm.config.firmware,
        "fixedPassthruHotPlugEnabled": vm.config.fixedPassthruHotPlugEnabled,
        "flags": {
            "disableAcceleration": vm.config.flags.disableAcceleration,
            "enableLogging": vm.config.flags.enableLogging,
            "useToe": vm.config.flags.useToe,
            "runWithDebugInfo": vm.config.flags.runWithDebugInfo,
            "monitorType": vm.config.flags.monitorType,
            "htSharing": vm.config.flags.htSharing,
            "snapshotDisabled": vm.config.flags.snapshotDisabled,
            "snapshotLocked": vm.config.flags.snapshotLocked,
            "diskUuidEnabled": vm.config.flags.diskUuidEnabled,
            "virtualMmuUsage": vm.config.flags.virtualMmuUsage,
            "virtualExecUsage": vm.config.flags.virtualExecUsage,
            "snapshotPowerOffBehavior": vm.config.flags.snapshotPowerOffBehavior,
            "recordReplayEnabled": vm.config.flags.recordReplayEnabled,
            "faultToleranceType": vm.config.flags.faultToleranceType,
            "cbrcCacheEnabled": vm.config.flags.cbrcCacheEnabled,
            "vvtdEnabled": vm.config.flags.vvtdEnabled,
            "vbsEnabled": vm.config.flags.vbsEnabled
        },
        "forkConfigInfo": vm.config.forkConfigInfo,
        "ftEncryptionMode": vm.config.ftEncryptionMode,
        "ftInfo": vm.config.ftInfo,
        "guestAutoLockEnabled": vm.config.guestAutoLockEnabled,
        "guestFullName": vm.config.guestFullName,
        "guestId": vm.config.guestId,
        "guestIntegrityInfo": {
            "enabled": vm.config.guestIntegrityInfo.enabled
        },
        "guestMonitoringModeInfo": {
            "gmmFile": vm.config.guestMonitoringModeInfo.gmmFile,
            "gmmAppliance": vm.config.guestMonitoringModeInfo.gmmAppliance
        },
        "hardware": {
            "numCPU": vm.config.hardware.numCPU,
            "numCoresPerSocket": vm.config.hardware.numCoresPerSocket,
            "autoCoresPerSocket": vm.config.hardware.autoCoresPerSocket,
            "memoryMB": vm.config.hardware.memoryMB,
            "virtualICH7MPresent": vm.config.hardware.virtualICH7MPresent,
            "virtualSMCPresent": vm.config.hardware.virtualSMCPresent,
            "device": [
                {
                    "key": item.key,
                    "deviceInfo": {
                        "label": item.deviceInfo.label,
                        "summary": item.deviceInfo.summary
                    },
                    "backing": item.backing,
                    "connectable": item.connectable,
                    "slotInfo": item.slotInfo,
                    "controllerKey": item.controllerKey,
                    "unitNumber": item.unitNumber,
                    "numaNode": item.numaNode,
                    "deviceGroupInfo": item.deviceGroupInfo,
                    #"busNumber": item.busNumber,
                    #"device": item.device
                } for item in vm.config.hardware.device
            ]
        },
        "hotPlugMemoryIncrementSize": vm.config.hotPlugMemoryIncrementSize,
        "hotPlugMemoryLimit": vm.config.hotPlugMemoryLimit,
        "initialOverhead": {
            "initialMemoryReservation": vm.config.initialOverhead.initialMemoryReservation,
            "initialSwapReservation": vm.config.initialOverhead.initialSwapReservation
        },
        "instanceUuid": vm.config.instanceUuid,
        "keyId": vm.config.keyId,
        "latencySensitivity": {
            "level": vm.config.latencySensitivity.level,
            "sensitivity": vm.config.latencySensitivity.sensitivity
        },
        "locationId": vm.config.locationId,
        "managedBy": vm.config.managedBy,
        "maxMksConnections": vm.config.maxMksConnections,
        "memoryAffinity": vm.config.memoryAffinity,
        "memoryAllocation": {
            "reservation": vm.config.memoryAllocation.reservation,
            "expandableReservation": vm.config.memoryAllocation.expandableReservation,
            "limit": vm.config.memoryAllocation.limit,
            "shares": {
                "shares": vm.config.memoryAllocation.shares.shares,
                "level": vm.config.memoryAllocation.shares.level
            },
            "overheadLimit": vm.config.memoryAllocation.overheadLimit
        },
        "memoryHotAddEnabled": vm.config.memoryHotAddEnabled,
        "memoryReservationLockedToMax": vm.config.memoryReservationLockedToMax,
        "messageBusTunnelEnabled": vm.config.messageBusTunnelEnabled,
        "migrateEncryption": vm.config.migrateEncryption,
        "modified": vm.config.modified,
        "name": vm.config.name,
        "nestedHVEnabled": vm.config.nestedHVEnabled,
        "networkShaper": vm.config.networkShaper,
        "npivDesiredNodeWwns": vm.config.npivDesiredNodeWwns,
        "npivDesiredPortWwns": vm.config.npivDesiredPortWwns,
        "npivNodeWorldWideName": vm.config.npivNodeWorldWideName,
        "npivOnNonRdmDisks": vm.config.npivOnNonRdmDisks,
        "npivPortWorldWideName": vm.config.npivPortWorldWideName,
        "npivTemporaryDisabled": vm.config.npivTemporaryDisabled,
        "npivWorldWideNameType": vm.config.npivWorldWideNameType,
        "numaInfo": vm.config.numaInfo,
        "pmem": vm.config.pmem,
        "pmemFailoverEnabled": vm.config.pmemFailoverEnabled,
        "rebootPowerOff": vm.config.rebootPowerOff,
        "repConfig": vm.config.repConfig,
        "scheduledHardwareUpgradeInfo": {
            "upgradePolicy": vm.config.scheduledHardwareUpgradeInfo.upgradePolicy,
            "versionKey": vm.config.scheduledHardwareUpgradeInfo.versionKey,
            "scheduledHardwareUpgradeStatus": vm.config.scheduledHardwareUpgradeInfo.scheduledHardwareUpgradeStatus,
            "fault": vm.config.scheduledHardwareUpgradeInfo.fault
        },
        "sevEnabled": vm.config.sevEnabled,
        "sgxInfo": {
            "epcSize": vm.config.sgxInfo.epcSize,
            "flcMode": vm.config.sgxInfo.flcMode,
            "lePubKeyHash": vm.config.sgxInfo.lePubKeyHash,
            "requireAttestation": vm.config.sgxInfo.requireAttestation
        },
        "swapPlacement": vm.config.swapPlacement,
        "swapStorageObjectId": vm.config.swapStorageObjectId,
        "template": vm.config.template,
        "tools": {
            "toolsVersion": vm.config.tools.toolsVersion,
            "toolsInstallType": vm.config.tools.toolsInstallType,
            "afterPowerOn": vm.config.tools.afterPowerOn,
            "afterResume": vm.config.tools.afterResume,
            "beforeGuestStandby": vm.config.tools.beforeGuestStandby,
            "beforeGuestShutdown": vm.config.tools.beforeGuestShutdown,
            "beforeGuestReboot": vm.config.tools.beforeGuestReboot,
            "toolsUpgradePolicy": vm.config.tools.toolsUpgradePolicy,
            "pendingCustomization": vm.config.tools.pendingCustomization,
            "customizationKeyId": vm.config.tools.customizationKeyId,
            "syncTimeWithHostAllowed": vm.config.tools.syncTimeWithHostAllowed,
            "syncTimeWithHost": vm.config.tools.syncTimeWithHost,
            "lastInstallInfo": {
                "counter": vm.config.tools.lastInstallInfo.counter,
                "fault": vm.config.tools.lastInstallInfo.fault
            }
        },
        "uuid": vm.config.uuid,
        "vAppConfig": vm.config.vAppConfig,
        "vAssertsEnabled": vm.config.vAssertsEnabled,
        "vFlashCacheReservation": vm.config.vFlashCacheReservation,
        "vPMCEnabled": vm.config.vPMCEnabled,
        "vcpuConfig": [
            {
                "key": item.key,
                "operation": item.operation,
                "level": item.level,
                "affinitySet": item.affinitySet,
                "numCpus": item.numCpus,
                "numCoresPerSocket": item.numCoresPerSocket
            } for item in vm.config.vcpuConfig
        ],
        "version": vm.config.version,
        "vmOpNotificationTimeout": vm.config.vmOpNotificationTimeout,
        "vmOpNotificationToAppEnabled": vm.config.vmOpNotificationToAppEnabled,
        "vmStorageObjectId": vm.config.vmStorageObjectId,
        "vmxConfigChecksum": vm.config.vmxConfigChecksum,
        "vmxStatsCollectionEnabled": vm.config.vmxStatsCollectionEnabled
    }

    print("Config:")
    for key, value in config_dict.items():
        print(f"    {key}: {value}")
    print("-" * 30)


    #return config_dict



def main():
    esxi_host = "10.14.45.11"
    username = "root"
    password = "Aa112233!"

    si = connect_to_vmware(esxi_host, username, password)

    is_running = True
    while is_running:
        print("\nMenü:")
        print("1- VM ID'leri Listele")
        print("2- Belirli VM ID'sine Göre Bilgileri Getir")
        print("3- Tüm VM Bilgilerini Getir")
        print("4- Çıkış")

        choice = input("Seçiminizi yapın (1-4): ")

        if choice == "1":
            list_vm_names_and_ids(si)
        elif choice == "2":
            vm_id = input("VM ID'sini girin: ")
            get_vm_info_by_id(si, vm_id)
        elif choice == "3":
            get_vm_info_all(si)
        elif choice == "4":
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçenek. Tekrar deneyin.")

    disconnect_from_vmware(si)

if __name__ == "__main__":
    main()


