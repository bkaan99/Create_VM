from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import base64
import psycopg2
import pandas as pd
import sys
from sqlalchemy import create_engine
from datetime import datetime


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

    new_list = ["bootOptions",
                "cpuAllocation",
                "defaultPowerOps",
                "files",
                "flags",
                "guestIntegrityInfo",
                "guestMonitoringModeInfo",
                "hardware",
                "initialOverhead",
                "latencySensitivity",
                "memoryAllocation",
                "scheduledHardwareUpgradeInfo",
                "sgxInfo",
                "tools"]

    vm_config_section = {f"{main_section}.{subsection}": getattr(vm.config, subsection) for subsection in
                           new_list}

    for section_name, section in vm_config_section.items():
        append_section_info(section, vmID, section_name)


    vm_config_vars = vars(vm.config)
    filtered_vm_config_vars = {key: value for key, value in vm_config_vars.items() if key not in new_list}

    for key, value in filtered_vm_config_vars.items():
        value = str(value)
        keyToInsert = key
        append_dataframe_given_values(keyToInsert, value, isDeletedValueForAppend, versionForAppend,
                                      createdDateForAppend, vmID, virtualizationEnvironmentType, esxi_host, None,
                                      notes=f"{main_section}")

    #datastoreUrl
    datastoreUrlDesc = vm.config.datastoreUrl
    for datastore in datastoreUrlDesc:
        append_section_info(datastore, vmID, "vm.config.datastoreUrl")

    #extraConfig
    extraConfigDesc = vm.config.extraConfig
    for config_id, config in enumerate(extraConfigDesc):
        append_section_info(config, vmID, f"vm.config.extraConfig.[{config_id}]")


    #hardware devices
    hardwareDevices = vm.config.hardware.device
    for device_count, device in enumerate(hardwareDevices):
        #deviceInfo
        deviceInfo = device.deviceInfo
        append_vm_info(vmID, "deviceInfo.label", deviceInfo.label, f"vm.config.hardware.device.deviceInfo.[{device_count}]")
        append_vm_info(vmID, "deviceInfo.summary", deviceInfo.summary, f"vm.config.hardware.device.deviceInfo.[{device_count}]")

        append_section_info(device, vmID, f"vm.config.hardware.device.[{device_count}]")


def datastore_section(vm, vmID):
    try:
        vmDatastore = vm.datastore
        for datastore_count,datastore in enumerate(vmDatastore):
            main_section = "vm.datastore"
            sub_sections = ["capability","info","summary"]
            addinational_list = ["alarmActionsEnabled",
                                "configStatus",
                                "name",
                                "overallStatus"]

            for item in addinational_list:
                append_vm_info(vmID, item, getattr(datastore, item), f"{main_section}.[{datastore_count}]")

            for section in sub_sections:
                append_section_info(getattr(datastore, section), vmID, f"{main_section}.[{datastore_count}].{section}")


            #declaredAlarmState
            declaredAlarmState = datastore.declaredAlarmState
            for alarm in declaredAlarmState:
                append_section_info(alarm, vmID, f"{main_section}.[{datastore_count}].declaredAlarmState")

            # #disabledMethod
            disabledMethod = datastore.disabledMethod
            for method in disabledMethod:
                append_vm_info(vmID, "disabledMethod", method, f"{main_section}.[{datastore_count}].disabledMethod")

            # #effectiveRole
            effectiveRole = datastore.effectiveRole
            for role in effectiveRole:
                append_vm_info(vmID, "effectiveRole", role, f"{main_section}.[{datastore_count}].effectiveRole")



            #host bilgisi
            all_host = datastore.host
            for host in all_host:
                #mountInfo
                mountInfo = host.mountInfo
                append_section_info(mountInfo, vmID, f"{main_section}.[{datastore_count}].host.mountInfo")

    except:
        pass

def vm_decalarmedstate_section(vm, vmID):
    vmDeclaredAlarmState = vm.declaredAlarmState
    for alarm_count, alarm in enumerate(vmDeclaredAlarmState):
        main_section = "vm.declaredAlarmState"
        description_list = ["acknowledged","acknowledgedByUser","acknowledgedTime","disabled",
                            "eventKey","key","overallStatus"]
        for item in description_list:
            append_vm_info(vmID, item, getattr(alarm, item), f"{main_section}.[{alarm_count}]")

        alarm_info = alarm.alarm.info
        important_info = ["actionFrequency","creationEventId","description","enabled","lastModifiedUser","name","systemName"]
        for item in important_info:
            append_vm_info(vmID, item, getattr(alarm_info, item), f"{main_section}.[{alarm_count}].alarm.info")


def vm_layout_section(vm, vmID):
    layout= vm.layout

    #configFile
    configFile = layout.configFile
    for count, file in enumerate(configFile):
        append_vm_info(vmID, f"configFile-{count}", file, "vm.layout.configFile")

    #diskFile
    disks = layout.disk
    for count, disk in enumerate(disks):
        diskFiles = disk.diskFile
        for count, file in enumerate(diskFiles):
            append_vm_info(vmID, f"diskFile-{count}", file, "vm.layout.disk.diskFile")

    #logFile
    logFiles = layout.logFile
    for count, file in enumerate(logFiles):
        append_vm_info(vmID, f"logFile-{count}", file, "vm.layout.logFile")

    #swapFile
    append_vm_info(vmID, "swapFile", layout.swapFile, "vm.layout.swapFile")

    #layoutFileEx
    layout_ex_file = vm.layoutEx.file
    for count, file in enumerate(layout_ex_file):
        append_section_info(file, vmID, f"vm.layoutEx.file.[{count}]")


def vm_information_getter(vms):
    for vm in vms:
        try:
            vmID = str(vm.summary.vm).split(":")[1].replace("'","")

            vmID = int(vmID.split('-')[-1])

        except:
            vmID = None


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
        # vm_config_section(vm, vmID)

        # #Datastore Section
        #datastore_section(vm, vmID)
        #
        # DeclaredAlarmState
        #vm_decalarmedstate_section(vm, vmID)

        # #DisabledMethod
        # for count, method in enumerate(vm.disabledMethod):
        #     append_vm_info(vmID, f"disabledMethod-{count}", method, "vm.disabledMethod")

        # # guest
        # append_section_info(vm.guest, vmID, "vm.guest")

        #guestHeartbeatStatus
        #append_vm_info(vmID, "guestHeartbeatStatus", vm.guestHeartbeatStatus, "vm")

        #layout description
        #vm_layout_section(vm, vmID)



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