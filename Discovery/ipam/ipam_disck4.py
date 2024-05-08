import warnings
import phpipamsdk
import psycopg2
import requests
from sqlalchemy import create_engine


def Connect_IPAM():
    warnings.filterwarnings('ignore')
    IPAM = phpipamsdk.PhpIpamApi(
        api_uri='https://172.28.0.27/api/0002/', api_verify_ssl=False)
    IPAM.login(auth=('ansible', 'Cekino123!'))
    token = IPAM._api_token

    return IPAM

def connect_Postgres():
    try:
        engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
        connectionForPostgres = psycopg2.connect(
            host="10.14.45.69",
            port="7100",
            database="karcin_pfms",
            user="postgres",
            password="Cekino.123!")
        cursorForPostgres = connectionForPostgres.cursor()

        return connectionForPostgres

    except psycopg2.OperationalError as e:
        print(f"Operasyon Hatası: {e}")
    except psycopg2.InterfaceError as e:
        print(f"Arayüz Hatası: {e}")
    except psycopg2.DatabaseError as e:
        print(f"Veritabanı Hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

    return None


def print_subnets(IPAM):

    subnets_url= IPAM._api_uri + 'subnets/?subnetId=107'
    response = requests.get(subnets_url, headers=IPAM._api_headers, verify=IPAM._api_verify_ssl)
    subnets = response.json()

    for subnet in subnets['data']:
        #sectionId = 2 IPV6
        #sectionId = 1 GlassHouse

        if subnet['sectionId'] == '1':
            print(subnet['id'], subnet['subnet']+"/"+subnet['mask'], subnet['description'])


def get_all_subnets(IPAM):
    subnets_url2=  phpipamsdk.SubnetsApi(phpipam=IPAM)
    subnets = subnets_url2.get_subnet()

    print("Subnets Bilgileri")


    for subnet in subnets['data']:
        if subnet['sectionId'] == '1':
            print("Subnet ID : ", subnet['id'])
            print("Subnet : ", subnet['subnet']+"/"+subnet['mask'],)
            print("Subnet Description : ", subnet['description'])
            #usage_description = get_subnet_usage(IPAM, subnet['id'])
            #print("Subnet Usage Percent %: ", usage_description['data']['Used_percent'])
            #get all ip addresses from subnet


            print(" ")
            print(" ")

            # print("Subnet Usage : ", subnets_url2.get_subnet_usage(subnet['id']))
            # print("Subnet Slaves : ", subnets_url2.list_subnet_slaves(subnet['id']))
            # print("Subnet Slaves Recursive : ", subnets_url2.list_subnet_slaves_recursive(subnet['id']))
            # print("Subnet Addresses : ", subnets_url2.list_subnet_addresses(subnet['id']))
            # print("Subnet First Free Address : ", subnets_url2.get_subnet_first_free_address(subnet['id']))
            # print("Subnet First Free Subnet : ", subnets_url2.get_subnet_first_free_subnet(subnet['id'], 24))
            # print("Subnet Last Free Subnet : ", subnets_url2.get_subnet_last_free_subnet(subnet['id'], 24))
            # print("Subnet Free Subnets : ", subnets_url2.list_subnet_free_subnets(subnet['id'], 24))
            # print("Subnet Address : ", subnets_url2.get_subnet_address(subnet['id'], ''))


def get_subnet(IPAM, subnet_id):
    subnets_url2=  phpipamsdk.SubnetsApi(phpipam=IPAM)
    subnet_info = subnets_url2.get_subnet(subnet_id= subnet_id)

    if subnet_info['data'] == []:
        print("Subnet ID: ", subnet_id + " " + "için bilgi bulunamadı")
        return None
    else:
        subnet_ip = subnet_info['data']['subnet']
        subnet_mask = subnet_info['data']['mask']
        return subnet_ip, subnet_mask


def get_subnet_usage(IPAM, subnet_id):
    subnets_url2=  phpipamsdk.SubnetsApi(phpipam=IPAM)
    return subnets_url2.get_subnet_usage(subnet_id= subnet_id)


def get_ip_addresses(IPAM):
    subnets_url2=  phpipamsdk.AddressesApi(phpipam=IPAM)
    ips = subnets_url2.get_address()

    print("IP Adresleri")
    for ip in ips['data']:
        print("IP ID : ", ip['id'])
        print("IP : ", ip['ip'])
        print("IP Description : ", ip['description'])
        print("IP Subnet ID : ", ip['subnetId'])
        print("Hostname : ", ip['hostname'])
        ping = subnets_url2.ping_address(ip['id'])['data']
        print("Ping : ", ping['success'])

        print(" ")

def get_ip_addresses_from_subnet(IPAM, subnet_id):
    subnets_url2=  phpipamsdk.SubnetsApi(phpipam=IPAM)
    ip_adresses = subnets_url2.list_subnet_addresses(subnet_id= subnet_id)
    print(" ")
    print(f"Subnet ID: {subnet_id}"'deki IP Adresleri: ')
    print("IP Adresleri: ")
    for ip in ip_adresses['data']:
        print("IP : ", ip['ip'])
        print("IP Description : ", ip['description'])
        print("IP Hostname : ", ip['hostname'])

def get_first_free_addresses_from_subnet(IPAM, subnet_id):
    try:
        subnets_url2=  phpipamsdk.AddressesApi(phpipam=IPAM)
        ip_adresses = subnets_url2.get_address_first_free(subnet_id= subnet_id)
        print(" ")
        print(f"Subnet ID: {subnet_id}" + " " + 'içerisindeki ilk boş IP Adresi: ')
        print("IP : ", ip_adresses['data'])

        return ip_adresses['data']
    except:
        print("IP Adresi Bulunamadı")
        return None


def check_ip_addres_with_hostname(IPAM, hostname):
    subnets_url2=  phpipamsdk.AddressesApi(phpipam=IPAM)
    ip_adresses = subnets_url2.search_hostname(hostname=hostname)
    if ip_adresses['data'] == []:
        print("Hostname: ", hostname + " " + "için IP Adresi Bulunamadı")
        return None
    else:
        print("ip Address: ", ip_adresses['data'][0]['ip'])
        ipam_ip = ip_adresses['data'][0]['ip']
        ipam_ip_subnet = ip_adresses['data'][0]['subnetId']

        return ipam_ip, ipam_ip_subnet


if __name__ == "__main__":
    IPAM = Connect_IPAM()

    #get_ip_addresses(IPAM)
    #get_all_subnets(IPAM)
    #print_subnets(IPAM)
    #get_ip_addresses_from_subnet(IPAM, 120)
    #get_first_free_addresses_from_subnet(IPAM, 120)


    check_ip_addres_with_hostname(IPAM, "Oprekin-PC")


    IPAM.logout()