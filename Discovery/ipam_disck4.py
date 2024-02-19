import warnings
import phpipamsdk
import requests

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
            usage_description = get_subnet_usage(IPAM, subnet['id'])
            print("Subnet Usage Percent %: ", usage_description['data']['Used_percent'])
            #get all ip addresses from subnet
            ip_adresses = subnets_url2.list_subnet_addresses(subnet['id'])
            print(" ")
            print("IP Adresleri: ")
            for ip in ip_adresses['data']:
                print("IP : ", ip['ip'])
                print("IP Description : ", ip['description'])
                print("IP Hostname : ", ip['hostname'])


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


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    IPAM = phpipamsdk.PhpIpamApi(
        api_uri='https://172.28.0.27/api/0002/', api_verify_ssl=False)
    IPAM.login(auth=('ansible', 'Cekino123!'))
    token = IPAM._api_token


    #get_ip_addresses(IPAM)
    get_all_subnets(IPAM)
    #print_subnets(IPAM)


    IPAM.logout()