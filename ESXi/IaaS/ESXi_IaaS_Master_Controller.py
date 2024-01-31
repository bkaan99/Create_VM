import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from ESXi.IaaS.Create import Create_Control_Plane
from ESXi.IaaS.Delete import delete_main


def connect_Postgres():
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()

    return connectionForPostgres


def get_vmList_Config():

    connectionForPostgres = connect_Postgres()
    VmListConfigrurationTable = pd.read_sql_query("select * from kr_vm_list where id=35",
                                                  connectionForPostgres)

    vmListConfig_Id = VmListConfigrurationTable.get("id")[0]
    vmListConfig_Cpu = VmListConfigrurationTable.get("cpu")[0]
    vmListConfig_RamSize = VmListConfigrurationTable.get("ramsizegb")[0]
    vmListConfig_VmName = VmListConfigrurationTable.get("vmname")[0]
    vmListConfig_HostName = VmListConfigrurationTable.get("hostname")[0]
    vmListConfig_IpAdress = VmListConfigrurationTable.get("ipaddress")[0]
    vmListConfig_Environment = VmListConfigrurationTable.get("environment")[0]
    vmListConfig_OperatingSystemInformation = VmListConfigrurationTable.get("operatingsysteminformation")[0]
    vmListConfig_OperatingSystemVersion = VmListConfigrurationTable.get("operatingsystemversion")[0]
    vmListConfig_InternetConnection = VmListConfigrurationTable.get("internetconnection")[0]
    vmListConfig_VirtualizationTechnology = VmListConfigrurationTable.get("virtualizationtechnology")[0]
    vmListConfig_PFMSConfigurationId = VmListConfigrurationTable.get("pfmsconfiguration_id")[0]

    return vmListConfig_OperatingSystemInformation, vmListConfig_VmName, vmListConfig_Cpu, vmListConfig_RamSize

def get_first_disik_Config():
    connectionForPostgres = connect_Postgres()
    VmFirstDiskConfigurationTable = pd.read_sql_query("select * from kr_vm_first_disk where vmlist_id=35",
                                                      connectionForPostgres)

    # vmFirstDiskConfig_Id = VmFirstDiskConfigurationTable.get("id")[0]
    # vmFirstDiskConfig_DiskByte = VmFirstDiskConfigurationTable.get("diskbyte")[0]
    # vmFirstDiskConfig_DiskSize = VmFirstDiskConfigurationTable.get("disksize")[0]
    # vmFirstDiskConfig_VmListId = VmFirstDiskConfigurationTable.get("vmlist_id")[0]
    # vmFirstDiskConfig_VmDiskImagePath = VmFirstDiskConfigurationTable.get("location")[0]
    # vmFirstDiskConfig_DiskType = VmFirstDiskConfigurationTable.get("controllerlocation")[0]

    return None

def IaaS_Create():
    vmListConfig_OperatingSystemInformation, vmListConfig_VmName, vmListConfig_Cpu, vmListConfig_RamSize = get_vmList_Config()

    if vmListConfig_OperatingSystemInformation == "Windows":
        template_name = "bkaan_deneme"
        Create_Control_Plane.main(copying_vm_name=template_name, cpu_count=vmListConfig_Cpu, memory_mb=vmListConfig_RamSize * 1024)

    elif vmListConfig_OperatingSystemInformation == "Linux":
        template_name = "Ubuntu_Deneme"
        Create_Control_Plane.main(copying_vm_name=template_name, cpu_count=vmListConfig_Cpu, memory_mb=vmListConfig_RamSize * 1024)

    elif vmListConfig_OperatingSystemInformation == "MacOS":
        pass

    else:
        pass


def IaaS_Delete():
    delete_main.main()

def IaaS_Update():
    pass


def main():

    user_select_mod = input("1- IaaS Create \n2- IaaS Delete \n3-IaaS Update\n")

    if user_select_mod == "1":
        IaaS_Create()

    elif user_select_mod == "2":
        IaaS_Delete()

    elif user_select_mod == "3":
        IaaS_Update()


if __name__ == "__main__":
    main()

