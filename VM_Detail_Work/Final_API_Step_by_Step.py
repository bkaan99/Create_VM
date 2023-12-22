from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# ESXi host bilgileri
esxi_host = "10.14.45.11"
username = "root"
password = "Aa112233!"

# Bağlantı yap
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_NONE  # Sertifika doğrulamasını devre dışı bırak

si = SmartConnect(host=esxi_host, user=username, pwd=password, port=443, sslContext=context)

# Sanal makineleri al
content = si.RetrieveContent()
container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vms = container.view


def get_capabilities():
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
    return capabilities

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
        "cpuFeatureMask": [
            {
                "dynamicType": item.dynamicType,
                "dynamicProperty": item.dynamicProperty,
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
                "dynamicType": item.dynamicType,
                "dynamicProperty": item.dynamicProperty,
                "name": item.name,
                "url": item.url
            } for item in vm.config.datastoreUrl
        ],
        "defaultPowerOps": {
            "dynamicType": vm.config.defaultPowerOps.dynamicType,
            "dynamicProperty": vm.config.defaultPowerOps.dynamicProperty,
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
        "dynamicProperty": vm.config.dynamicProperty,
        "dynamicType": vm.config.dynamicType,
        "extraConfig": [
            {
                "key": item.key,
                "value": item.value
            } for item in vm.config.extraConfig
        ],
        "files": {
            "dynamicType": vm.config.files.dynamicType,
            "dynamicProperty": vm.config.files.dynamicProperty,
            "vmPathName": vm.config.files.vmPathName,
            "snapshotDirectory": vm.config.files.snapshotDirectory,
            "suspendDirectory": vm.config.files.suspendDirectory,
            "logDirectory": vm.config.files.logDirectory,
            "ftMetadataDirectory": vm.config.files.ftMetadataDirectory
        },
        "firmware": vm.config.firmware,
        "fixedPassthruHotPlugEnabled": vm.config.fixedPassthruHotPlugEnabled,
        "flags": {
            "dynamicType": vm.config.flags.dynamicType,
            "dynamicProperty": vm.config.flags.dynamicProperty,
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
            "dynamicType": vm.config.guestIntegrityInfo.dynamicType,
            "dynamicProperty": vm.config.guestIntegrityInfo.dynamicProperty,
            "enabled": vm.config.guestIntegrityInfo.enabled
        },
        "guestMonitoringModeInfo": {
            "dynamicType": vm.config.guestMonitoringModeInfo.dynamicType,
            "dynamicProperty": vm.config.guestMonitoringModeInfo.dynamicProperty,
            "gmmFile": vm.config.guestMonitoringModeInfo.gmmFile,
            "gmmAppliance": vm.config.guestMonitoringModeInfo.gmmAppliance
        },
        "hardware": {
            "dynamicType": vm.config.hardware.dynamicType,
            "dynamicProperty": vm.config.hardware.dynamicProperty,
            "numCPU": vm.config.hardware.numCPU,
            "numCoresPerSocket": vm.config.hardware.numCoresPerSocket,
            "autoCoresPerSocket": vm.config.hardware.autoCoresPerSocket,
            "memoryMB": vm.config.hardware.memoryMB,
            "virtualICH7MPresent": vm.config.hardware.virtualICH7MPresent,
            "virtualSMCPresent": vm.config.hardware.virtualSMCPresent,
            "device": [
                {
                    "dynamicType": item.dynamicType,
                    "dynamicProperty": item.dynamicProperty,
                    "key": item.key,
                    "deviceInfo": {
                        "dynamicType": item.deviceInfo.dynamicType,
                        "dynamicProperty": item.deviceInfo.dynamicProperty,
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
            "dynamicType": vm.config.initialOverhead.dynamicType,
            "dynamicProperty": vm.config.initialOverhead.dynamicProperty,
            "initialMemoryReservation": vm.config.initialOverhead.initialMemoryReservation,
            "initialSwapReservation": vm.config.initialOverhead.initialSwapReservation
        },
        "instanceUuid": vm.config.instanceUuid,
        "keyId": vm.config.keyId,
        "latencySensitivity": {
            "dynamicType": vm.config.latencySensitivity.dynamicType,
            "dynamicProperty": vm.config.latencySensitivity.dynamicProperty,
            "level": vm.config.latencySensitivity.level,
            "sensitivity": vm.config.latencySensitivity.sensitivity
        },
        "locationId": vm.config.locationId,
        "managedBy": vm.config.managedBy,
        "maxMksConnections": vm.config.maxMksConnections,
        "memoryAffinity": vm.config.memoryAffinity,
        "memoryAllocation": {
            "dynamicType": vm.config.memoryAllocation.dynamicType,
            "dynamicProperty": vm.config.memoryAllocation.dynamicProperty,
            "reservation": vm.config.memoryAllocation.reservation,
            "expandableReservation": vm.config.memoryAllocation.expandableReservation,
            "limit": vm.config.memoryAllocation.limit,
            "shares": {
                "dynamicType": vm.config.memoryAllocation.shares.dynamicType,
                "dynamicProperty": vm.config.memoryAllocation.shares.dynamicProperty,
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
            "dynamicType": vm.config.scheduledHardwareUpgradeInfo.dynamicType,
            "dynamicProperty": vm.config.scheduledHardwareUpgradeInfo.dynamicProperty,
            "upgradePolicy": vm.config.scheduledHardwareUpgradeInfo.upgradePolicy,
            "versionKey": vm.config.scheduledHardwareUpgradeInfo.versionKey,
            "scheduledHardwareUpgradeStatus": vm.config.scheduledHardwareUpgradeInfo.scheduledHardwareUpgradeStatus,
            "fault": vm.config.scheduledHardwareUpgradeInfo.fault
        },
        "sevEnabled": vm.config.sevEnabled,
        "sgxInfo": {
            "dynamicType": vm.config.sgxInfo.dynamicType,
            "dynamicProperty": vm.config.sgxInfo.dynamicProperty,
            "epcSize": vm.config.sgxInfo.epcSize,
            "flcMode": vm.config.sgxInfo.flcMode,
            "lePubKeyHash": vm.config.sgxInfo.lePubKeyHash,
            "requireAttestation": vm.config.sgxInfo.requireAttestation
        },
        "swapPlacement": vm.config.swapPlacement,
        "swapStorageObjectId": vm.config.swapStorageObjectId,
        "template": vm.config.template,
        "tools": {
            "dynamicType": vm.config.tools.dynamicType,
            "dynamicProperty": vm.config.tools.dynamicProperty,
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
                "dynamicType": vm.config.tools.lastInstallInfo.dynamicType,
                "dynamicProperty": vm.config.tools.lastInstallInfo.dynamicProperty,
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
                "dynamicType": item.dynamicType,
                "dynamicProperty": item.dynamicProperty,
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

# Sanal makineleri listeleyerek tüm detayları ekrana yazdır
print("Sanal Makineler:")

for vm in vms:

    capabilities = get_capabilities()
    # for key, value in capabilities.items():
    #     print(f"{key}: {value}")
    # print("-" * 30)



# Bağlantıyı kapat
Disconnect(si)
