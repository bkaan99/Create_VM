import socket
import time
import warnings
import phpipamsdk
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from Discovery import Credentials

def is_connected(host, port):
    try:
        # Bir soket nesnesi oluştur ve belirtilen host ve port'a bağlanmaya çalış
        with socket.create_connection((host, port), timeout=5) as connection:
            return True
    except (socket.gaierror, socket.timeout, ConnectionRefusedError):
        return False

def Connect_IPAM(ipam_api_url, ipam_login):
    warnings.filterwarnings('ignore')
    if is_connected('172.28.0.27', 443):
        try:
            IPAM = phpipamsdk.PhpIpamApi(
                api_uri=ipam_api_url, api_verify_ssl=False)
            IPAM.login(auth=(ipam_login['username'], ipam_login['password']))
            token = getattr(IPAM, '_api_token', None)
            if token is None:
                raise AttributeError("Token attribute not found")
            return IPAM

        except Exception as e:
            print(f"Bağlantı Hatası: {e}")
    else:
        print("IPAM'a bağlanılamadı")
        return None


def get_ip_addresses(IPAM):
    subnets_url2 = phpipamsdk.AddressesApi(phpipam=IPAM)
    ips = subnets_url2.get_address()

    if ips['success'] is True:
        for count, ip in enumerate(ips['data']):
            print(count)
            for key, value in (item for item in ip.items() if item[0] not in ["links"]):
                append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend,
                                              createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url,
                                              "Adresses", f"{ipam_api_url}adresses/{ip['id']}")

            # ping = subnets_url2.ping_address(ip['id'])['data']
            # append_dataframe_given_values("ping", str(ping['result_code']), isDeletedValueForAppend, versionForAppend,
            #                               createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url,
            #                               "Adresses/Ping", f"{ipam_api_url}adresses/{ip['id']}")

            percentage = (count / len(ips['data'])) * 100
            percentage_formatted = "{:.2f}".format(percentage)
            print("Process Percentage : ", percentage_formatted, "%")
    else:
        print("IP Adresleri Bulunamadı")
        return None

def get_all_subnets(IPAM):
    subnets_url2=  phpipamsdk.SubnetsApi(phpipam=IPAM)
    subnets = subnets_url2.get_subnet()

    start_time = time.time()

    if subnets['success'] is True:
        for count, subnet in enumerate(subnets['data']):
            print(count)
            for key, value in (item for item in subnet.items() if item[0] not in ["links", "permissions"]):
                append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Subnets", f"{ipam_api_url}subnets/{subnet['id']}")

            #subnet permissions bilgisi
            for perm in subnet['permissions']:
                for key, value in perm.items():
                    append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Subnets/Permissions", f"{ipam_api_url}subnets/{subnet['id']}")

            #subnet usage bilgisi
            subnet_usage = subnets_url2.get_subnet_usage(subnet_id=subnet['id'])

            if subnet_usage['success'] is True:
                for key, value in subnet_usage['data'].items():
                    append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Subnets/Usage", f"{ipam_api_url}subnets/{subnet['id']}")

            #subnete ait ip adresleri
            ip_adresses = subnets_url2.list_subnet_addresses(subnet_id=subnet['id'])
            if ip_adresses['success'] is True:
                for ip in ip_adresses['data']:
                    append_dataframe_given_values("ip", str(ip['ip']), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Subnets/Adresses", f"{ipam_api_url}subnets/{subnet['id']}/adresses/{ip['id']}")

            # Kalan süre ve yüzdelik hesaplama bilgisi
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_subnets = len(subnets['data']) - count - 1
            if count > 0:
                avg_time_per_subnet = elapsed_time / count
                remaining_time = avg_time_per_subnet * remaining_subnets
            else:
                remaining_time = 0

            percentage = (count / len(subnets['data'])) * 100
            percentage_formatted = "{:.2f}".format(percentage)
            print("Process Percentage : ", percentage_formatted, "%")
            print("Elapsed Time:", "{:.2f}".format(elapsed_time), "seconds")
            print("Remaining Time:", "{:.2f}".format(remaining_time), "seconds")

    else:
        print("Subnetler Bulunamadı")
        return None

def get_sections(IPAM):
    sections_url2=  phpipamsdk.SectionsApi(phpipam=IPAM)
    sections = sections_url2.list_sections()

    if sections['success'] is True:
        for count, section in enumerate(sections['data']):
            print(count)
            for key, value in (item for item in section.items() if item[0] not in ["links"]):
                append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Sections", f"{ipam_api_url}sections/{section['id']}")

            # Kalan süre ve yüzdelik hesaplama bilgisi
            percentage = (count / len(sections['data'])) * 100
            percentage_formatted = "{:.2f}".format(percentage)
            print("Process Percentage : ", percentage_formatted, "%")

    else:
        print("Sectionlar Bulunamadı")
        return None

def get_circiuts(IPAM):
    try:
        circuits_url2=  phpipamsdk.CircuitsApi(phpipam=IPAM)
        circuits = circuits_url2.list_circuits()

        if circuits['success'] is True:
            for count, circuit in enumerate(circuits['data']):
                print(count)
                for key, value in (item for item in circuit.items() if item[0] not in ["links"]):
                    append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Circuits", f"{ipam_api_url}circuits/{circuit['id']}")

        providers = circuits_url2.list_providers()
        if providers['success'] is True:
            for provider in providers['data']:
                for key, value in provider.items():
                    append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Circuits/Providers", f"{ipam_api_url}circuits/providers/{provider['id']}")
        else:
            print("Circuitler Bulunamadı")
            return None

    except Exception as e:
        print(f"Circuitler Bulunamadı: {e}")
        return None


def get_devices(IPAM):
    devices_url2=  phpipamsdk.DevicesApi(phpipam=IPAM)
    devices = devices_url2.list_devices()

    if devices['success'] is True:
        for count, device in enumerate(devices['data']):
            print(count)
            for key, value in (item for item in device.items() if item[0] not in ["links"]):
                append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Devices", f"{ipam_api_url}devices/{device['id']}")

            # Kalan süre ve yüzdelik hesaplama bilgisi
            percentage = (count / len(devices['data'])) * 100
            percentage_formatted = "{:.2f}".format(percentage)
            print("Process Percentage : ", percentage_formatted, "%")

    else:
        print("Cihazlar Bulunamadı")
        return None

def get_vlan(IPAM):
    vlans_url2=  phpipamsdk.VlansApi(phpipam=IPAM)
    vlans = vlans_url2.list_vlans()

    if vlans['success'] is True:
        for count, vlan in enumerate(vlans['data']):
            print(count)
            for key, value in (item for item in vlan.items() if item[0] not in ["links"]):
                append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Vlans", f"{ipam_api_url}vlans/{vlan['id']}")

            # Kalan süre ve yüzdelik hesaplama bilgisi
            percentage = (count / len(vlans['data'])) * 100
            percentage_formatted = "{:.2f}".format(percentage)
            print("Process Percentage : ", percentage_formatted, "%")

            vlan_subnets = vlans_url2.list_vlan_subnets(vlan_id=vlan['id'])
            if vlan_subnets['success'] is True:
                for subnet in vlan_subnets['data']:
                    for key, value in (item for item in subnet.items() if item[0] not in ["links"]):
                        append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "Vlans/Subnets", f"{ipam_api_url}vlans/{vlan['id']}/subnets/{subnet['id']}")

    else:
        print("Vlanlar Bulunamadı")
        return None

def get_l2domains(IPAM):
    l2domains_url2=  phpipamsdk.L2DomainsApi(phpipam=IPAM)
    l2domains = l2domains_url2.list_l2domains()

    if l2domains['success'] is True:
        for count, l2domain in enumerate(l2domains['data']):
            print(count)
            for key, value in (item for item in l2domain.items() if item[0] not in ["links"]):
                append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "L2Domains", f"{ipam_api_url}l2domains/{l2domain['id']}")

            # Kalan süre ve yüzdelik hesaplama bilgisi
            percentage = (count / len(l2domains['data'])) * 100
            percentage_formatted = "{:.2f}".format(percentage)
            print("Process Percentage : ", percentage_formatted, "%")

            vlans = l2domains_url2.get_l2domain_vlans(domain_id=l2domain['id'])
            if vlans['success'] is True:
                for vlan in vlans['data']:
                    for key, value in (item for item in vlan.items() if item[0] not in ["links"]):
                        append_dataframe_given_values(str(key), str(value), isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, ipam_base_url, "L2Domains/Vlans", f"{ipam_api_url}l2domains/{l2domain['id']}/vlans/{vlan['vlanId']}")


    else:
        print("L2Domainlar Bulunamadı")
        return None

def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[key,value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]

def vm_information_getter():

    get_ip_addresses(IPAM)
    get_all_subnets(IPAM)
    get_sections(IPAM)
    get_circiuts(IPAM)
    get_devices(IPAM)
    get_vlan(IPAM)
    get_l2domains(IPAM)

if __name__ == "__main__":
    ipam_login, ipam_api_url, ipam_base_url = Credentials.ipam_credential()
    IPAM = Connect_IPAM(ipam_api_url, ipam_login)

    createdDateForAppend = datetime.now()
    versionForAppend = 2
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "IPAM"

    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')

    connectionForPostgres = psycopg2.connect(
        host="10.14.45.69",
        port="7100",
        database="karcin_pfms",
        user="postgres",
        password="Cekino.123!")
    cursorForPostgres = connectionForPostgres.cursor()
    vm_information_getter()

    #export csv
    dataFrameForInsert.to_csv("subnets.csv", index=False)

    dataFrameForInsert.to_sql("ipam_disc", engineForPostgres, chunksize=5000, index=False, method=None,if_exists='append')