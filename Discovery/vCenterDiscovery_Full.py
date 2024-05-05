from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import base64
import psycopg2
import pandas as pd
import sys
from sqlalchemy import create_engine
from datetime import datetime
from tqdm import tqdm


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def connect_esxi_environment(esxi_host, username, password):
    # Bağlantı yap
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_NONE  # Sertifika doğrulamasını devre dışı bırak

    si = SmartConnect(host=esxi_host, user=username, pwd=password, port=443, sslContext=context)

    # Sanal makineleri al
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    return vms, si

def append_vm_info(vmID, key, value, additional_info=''):
    try:
        append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes=f"{additional_info}")
    except:
        pass

def append_section_info(section, vmID, section_name):
    try:
        section_info = vars(section)
        filtered_info = {key: value for key, value in section_info.items() if key not in ['dynamicProperty', 'dynamicType']}
        for key, value in filtered_info.items():
            value = str(value)
            keyToInsert = key
            append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                          notes=f"{section_name}")
    except:
        pass

def vm_summary_section(vm, vmID):
    main_section = "vm.summary"
    sub_sections = ["config",
                    "guest",
                    "overallStatus",
                    "quickStats",
                    "runtime",
                    "storage"]

    vm_summary_sections = {f"{main_section}.{subsection}": getattr(vm.summary, subsection) for subsection in
                           sub_sections}

    for section_name, section in vm_summary_sections.items():
        append_section_info(section, vmID, section_name)


def vm_config_section(vm, vmID):
    main_section = "vm.config"
    sub_sections = [
    "alternateGuestName",
    "annotation",
    "bootOptions",
    "changeTrackingEnabled",
    "changeVersion",
    "consolePreferences",
    "contentLibItemInfo",
    "cpuAffinity",
    "cpuAllocation",
    "cpuFeatureMask",
    "cpuHotAddEnabled",
    "cpuHotRemoveEnabled",
    "createDate",
    "defaultPowerOps",
    "deviceGroups",
    "deviceSwap",
    "files",
    "firmware",
    "fixedPassthruHotPlugEnabled",
    "forkConfigInfo",
    "ftEncryptionMode",
    "ftInfo",
    "guestAutoLockEnabled",
    "guestFullName",
    "guestId",
    "guestIntegrityInfo",
    "guestMonitoringModeInfo",
    "hardware",
    "hotPlugMemoryIncrementSize",
    "hotPlugMemoryLimit",
    "initialOverhead",
    "instanceUuid",
    "keyId",
    "latencySensitivity",
    "locationId",
    "managedBy",
    "maxMksConnections",
    "memoryAffinity",
    "memoryAllocation",
    "memoryHotAddEnabled",
    "memoryReservationLockedToMax",
    "messageBusTunnelEnabled",
    "migrateEncryption",
    "modified",
    "name",
    "nestedHVEnabled",
    "networkShaper",
    "npivDesiredNodeWwns",
    "npivDesiredPortWwns",
    "npivNodeWorldWideName",
    "npivOnNonRdmDisks",
    "npivPortWorldWideName",
    "npivTemporaryDisabled",
    "npivWorldWideNameType",
    "numaInfo",
    "pmem",
    "pmemFailoverEnabled",
    "repConfig",
    "rebootPowerOff",
    "scheduledHardwareUpgradeInfo",
    "sevEnabled",
    "sgxInfo",
    "swapPlacement",
    "swapStorageObjectId",
    "template",
    "tools",
    "uuid",
    "vAppConfig",
    "vAssertsEnabled",
    "vFlashCacheReservation",
    "version",
    "vmOpNotificationTimeout",
    "vmOpNotificationToAppEnabled",
    "vmStorageObjectId",
    "vmxConfigChecksum",
    "vmxStatsCollectionEnabled"
]

    extra_sub_sections = [
        "cpuAllocation.shares"
        ]

    vm_config_section = {f"{main_section}.{subsection}": getattr(vm.config, subsection) for subsection in
                           sub_sections}

    for section_name, section in vm_config_section.items():
        append_section_info(section, vmID, section_name)

    #datastoreUrl
    datastoreUrlDesc = vm.config.datastoreUrl
    for datastore in datastoreUrlDesc:
        append_section_info(datastore, vmID, "vm.config.datastoreUrl")

    #extraConfig
    extraConfigDesc = vm.config.extraConfig
    config_id = 0
    for config in extraConfigDesc:
        append_section_info(config, vmID, f"vm.config.extraConfig.[{config_id}]")
        config_id += 1

def datastore_section(vm, vmID):
    try:
        vmDatastore = vm.datastore
        for datastore in vmDatastore:
            try:
                datastoreAlarmActions = datastore.alarmActionsEnabled
                keyToInsert = "alarmActionsEnabled"
                append_dataframe_given_values(keyToInsert, datastoreAlarmActions, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                              "vm.datastore.datastoreAlarmActions")
            except:
                pass

            try:
                datastoreCapabilities = vars(datastore.capability)
                for key, value in datastoreCapabilities.items():
                    value = str(value)
                    keyToInsert = key
                    append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                  "vm.datastore.capability")
            except:
                pass

            try:
                datastoreConfigStatus = datastore.configStatus
                keyToInsert = "configStatus"
                append_dataframe_given_values(keyToInsert, datastoreConfigStatus, isDeletedValueForAppend, versionForAppend,
                                                createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                "vm.datastore.configStatus")
            except:
                pass

            try:
                declaredAlarmState = datastore.declaredAlarmState
                for alarm in declaredAlarmState:
                    alarmDesc = vars(alarm)
                    for key, value in alarmDesc.items():
                        value = str(value)
                        keyToInsert = key
                        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                      "vm.datastore.declaredAlarmState")
            except:
                pass

            #disabledMethod
            try:
                disabledMethod = datastore.disabledMethod
                for method in disabledMethod:
                    keyToInsert = "disabledMethod"
                    append_dataframe_given_values(keyToInsert, method, isDeletedValueForAppend, versionForAppend,
                                                  createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                                  "vm.datastore.disabledMethod")
            except:
                pass

            #effectiveRole
            try:
                effectiveRole = datastore.effectiveRole
                keyToInsert = "effectiveRole"
                append_dataframe_given_values(keyToInsert, effectiveRole, isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                              "vm.datastore.effectiveRole")
            except:
                pass

            #host bilgisi
            try:
                all_host = datastore.host
                for host in all_host:
                    #key bilgisi


                    #mountInfo
                    try:
                        mountInfo = vars(host.mountInfo)
                        for key, value in mountInfo.items():
                            value = str(value)
                            keyToInsert = key
                            append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                                          createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host,
                                                          None,
                                                          "vm.datastore.host.mountInfo")
                    except:
                        pass


            except:
                pass

    except:
        pass


def vm_information_getter(vms):
    for vm in vms:
        try:
            vmID = str(vm.summary.vm).split(":")[1].replace("'","")

            vmID = int(vmID.split('-')[-1])

        except:
            vmID = None

        vm_config_section(vm, vmID)

        # #alarmactionenabled description
        # append_vm_info(vmID, "alarmActionsEnabled", vm.alarmActionsEnabled, "vm.alarmActionsEnabled")
        #
        # # Summary Section
        # vm_summary_section(vm, vmID)
        #
        # #Capability Section
        # append_section_info(vm.capability, vmID, "vm.capability")
        #
        # #Config Section
        # config = vars(vm.config)
        # for key, value in config.items():
        #     value = str(value)
        #     keyToInsert = key
        #     append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
        #                                   createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
        #                                   notes="vm.config")
        #
        # #Config Status
        # vmConfigStatus = vm.configStatus
        # keyToInsert = "configStatus"
        # append_dataframe_given_values(keyToInsert, vmConfigStatus, isDeletedValueForAppend, versionForAppend,
        #                                   createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
        #                                   notes="vm.configStatus")
        #
        # #Datastore Section
        # datastore_section(vm, vmID)
        #
        #
        #



if __name__ == "__main__":
    createdDateForAppend = datetime.now()
    versionForAppend = 1
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "vCenter"
    esxi_host = "10.14.45.10"
    username = "administrator@vsphere.local"
    password = "Aa112233!"
    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    mystring = base64.b64decode(sys.argv[1]).decode('UTF-8')
    mystring = mystring.replace("[", "").replace("]", "")

    def Convert(string):
        li = list(string.replace(' ', '').split(","))
        return li

    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()
    vmIdList = Convert(mystring)
    vmsFromESXI, si = connect_esxi_environment(esxi_host, username, password)
    vm_information_getter(vmsFromESXI)
    Disconnect(si)
    dataFrameForInsert.to_sql("vcenter_disc", engineForPostgres, chunksize=5000, index=False, method=None,
                              if_exists='append')