import requests
import configparser
import logging
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(filename='firewall_details.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def flatten_dict(d, parent_key='', sep='_'):
    if not d:
        return {parent_key: ''}
    else:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())

            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict) and 'name' in item:
                        items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
                    else:
                        items.append((f"{new_key}{sep}{i}", item))

            else:
                items.append((new_key, v))
        return dict(items)

def log_and_print(message):
    """Log and print the message to both file and console."""
    print(message)
    logging.info(message)


def read_config(config_file_path=r'C:\Projeler\py\py_FIREWALL\firewall_config.ini'):
    """Read the configuration from an INI file."""
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return {
        'url': config['fortigate']['url'],
        'access_token': config['fortigate']['access_token']
    }


def get_all_vlans_details(config):
    """Fetch all VLAN details from FortiGate."""
    url = config['url']
    access_token = config['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    endpoint = '/api/v2/cmdb/system/interface'
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)

    if response.status_code == 200:
        vlans = response.json()['results']
        all_vlans_details = []

        for vlan in vlans:
            vlan_details = {
                'Name': vlan.get('name', 'N/A') ,
                'VLAN ID': vlan.get('vlanid', 'N/A'),
                'Interface': vlan.get('interface', 'N/A'),
                'IP Address': vlan.get('ip', 'N/A'),
                'Status': vlan.get('status', 'N/A'),
                'Alias': vlan.get('alias', 'N/A'),
                'MAC Address': vlan.get('macaddr', 'N/A'),
                'VLAN Interface': vlan.get('vlaninterface', 'N/A'),
                'Role': vlan.get('role', 'N/A'),
                'Type': vlan.get('type', 'N/A'),
                'MTU': vlan.get('mtu', 'N/A'),
                'Description': vlan.get('description', 'N/A'),
                'Speed': vlan.get('speed', 'N/A'),
                'Duplex': vlan.get('duplex', 'N/A'),
                'DHCP Relay IP': vlan.get('dhcp-relay-ip', 'N/A'),
                'DHCP Relay Service': vlan.get('dhcp-relay-service', 'N/A'),
                'DHCP Client Options': vlan.get('dhcp-client-options', 'N/A'),
                'Management IP': vlan.get('management-ip', 'N/A'),
                'IPv6 Address': vlan.get('ipv6', {}).get('ip6-address', 'N/A'),
                'IPv6 Gateway': vlan.get('ipv6', {}).get('ip6-gateway', 'N/A'),
                'Firewall Rules': [],
                'Web Filter Profiles': [],
                'App Control Profiles': []
            }

            # Bandwidth bilgilerini almak için ek bir API çağrısı
            traffic_endpoint = f"/api/v2/monitor/system/interface/select?filter=name=={vlan.get('name', '')}"
            traffic_response = requests.get(f"{url}{traffic_endpoint}", headers=headers, verify=False)
            if traffic_response.status_code == 200:
                traffic_data = traffic_response.json()
                vlan_details.update({
                    'RX Bandwidth': traffic_data.get('rx', 'N/A'),
                    'TX Bandwidth': traffic_data.get('tx', 'N/A')
                })
            else:
                vlan_details.update({
                    'RX Bandwidth': 'N/A',
                    'TX Bandwidth': 'N/A'
                })

            all_vlans_details.append(vlan_details)

        return all_vlans_details
    else:
        log_and_print(f"Error fetching VLAN details: {response.status_code}")
        return None


def get_firewall_rules(config):
    """Fetch all firewall rules from FortiGate."""
    url = config['url']
    access_token = config['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    endpoint = '/api/v2/cmdb/firewall/policy'
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)

    if response.status_code == 200:
        rules = response.json()['results']
        all_rules_details = []
        x_list = []

        for rule in rules:
            x = flatten_dict(rule)
            rule_details = {
                'ID': rule.get('policyid', 'N/A'),
                'Name': rule.get('name', 'N/A'),
                'Source Interface': [src.get('name', 'N/A') for src in rule.get('srcintf', [])],
                'Destination Interface': [dst.get('name', 'N/A') for dst in rule.get('dstintf', [])],
                'Source Address': [src.get('name', 'N/A') for src in rule.get('srcaddr', [])],
                'Destination Address': [dst.get('name', 'N/A') for dst in rule.get('dstaddr', [])],
                'Service': [srv.get('name', 'N/A') for srv in rule.get('service', [])],
                'Action': rule.get('action', 'N/A'),
                'Status': rule.get('status', 'N/A')
            }
            all_rules_details.append(rule_details)
            x_list.append(x)

        return all_rules_details, x_list
    else:
        log_and_print(f"Error fetching firewall rules: {response.status_code}")
        return None

def get_adresses(config):
    """Fetch all firewall rules from FortiGate."""
    url = config['url']
    access_token = config['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    endpoint = '/api/v2/cmdb/firewall/address'
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)

    if response.status_code == 200:
        adresses = response.json()['results']
        x_list = []

        for adress in adresses:
            x = flatten_dict(adress)
            x_list.append(x)

        return x_list
    else:
        log_and_print(f"Error fetching adresses: {response.status_code}")
        return None


def get_services_tab(config):
    """Fetch all firewall rules from FortiGate."""
    url = config['url']
    access_token = config['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    endpoint = '/api/v2/cmdb/firewall.service/custom'
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)

    if response.status_code == 200:
        services_tab = response.json()['results']
        x_list = []

        for tab in services_tab:
            x = flatten_dict(tab)
            x_list.append(x)

        return x_list
    else:
        log_and_print(f"Error fetching adresses: {response.status_code}")
        return None


def get_web_filter_profiles(config):
    """Fetch all web filter profiles from FortiGate."""
    url = config['url']
    access_token = config['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    endpoint = '/api/v2/cmdb/webfilter/profile'
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)

    if response.status_code == 200:
        profiles = response.json()['results']
        all_profiles_details = []

        for profile in profiles:
            profile_details = {
                'Name': profile.get('name', 'N/A'),
                'Comment': profile.get('comments', 'N/A'),
                'Categories': [cat.get('id', 'N/A') for cat in profile.get('filter', [])]
            }
            all_profiles_details.append(profile_details)

        return all_profiles_details
    else:
        log_and_print(f"Error fetching web filter profiles: {response.status_code}")
        return None


def get_app_control_profiles(config):
    """Fetch all application control profiles from FortiGate."""
    url = config['url']
    access_token = config['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    endpoint = '/api/v2/cmdb/application/list'
    response = requests.get(f"{url}{endpoint}", headers=headers, verify=False)

    if response.status_code == 200:
        profiles = response.json()['results']
        all_profiles_details = []

        for profile in profiles:
            profile_details = {
                'Name': profile.get('name', 'N/A'),
                'Comment': profile.get('comment', 'N/A'),
                'Applications': [app.get('name', 'N/A') for app in profile.get('entries', [])]
            }
            all_profiles_details.append(profile_details)

        return all_profiles_details
    else:
        log_and_print(f"Error fetching application control profiles: {response.status_code}")
        return None


def map_rules_to_vlans(vlans, x_list):
    """Map firewall rules to their respective VLANs based on interfaces."""
    for vlan in vlans:
        vlan_name = vlan['Name']
        append_rule = False
        for x in x_list:
            for k, v in x.items():
                if k.startswith('srcintf_') and vlan_name in v:
                    append_rule = True
                    break
                elif k.startswith('dstintf_') and vlan_name in v:
                    append_rule = True
                    break
            if append_rule:
                vlan['Firewall Rules'].append(x)

    return vlans


def map_profiles_to_vlans(vlans, web_profiles, app_profiles):
    """Map web filter and app control profiles to their respective VLANs."""
    for vlan in vlans:
        vlan_name = vlan['Name']
        for profile in web_profiles:
            if vlan_name in profile['Name']:
                vlan['Web Filter Profiles'].append(profile)
        for profile in app_profiles:
            if vlan_name in profile['Name']:
                vlan['App Control Profiles'].append(profile)
    return vlans


def save_to_json(data, filename):
    """Save the collected data to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        log_and_print(f"Data successfully saved to {filename}")
    except Exception as e:
        log_and_print(f"Error saving data to file: {e}")


def main_controller():
    config_path = r'/Users/b.gurgen/PycharmProjects/Create_VM/Discovery/firewall/config.ini'
    config = read_config(config_path)

    vlan_details = get_all_vlans_details(config)
    firewall_rules, x_list = get_firewall_rules(config)
    adresses = get_adresses(config)
    services_tab = get_services_tab(config)
    web_filter_profiles = get_web_filter_profiles(config)
    app_control_profiles = get_app_control_profiles(config)

    if vlan_details and firewall_rules and web_filter_profiles and app_control_profiles:
        combined_details = map_rules_to_vlans(vlan_details, x_list)
        combined_details = map_profiles_to_vlans(combined_details, web_filter_profiles, app_control_profiles)
        #save_to_json(combined_details, "firewall_details.json")
        log_and_print("VLAN, Firewall, Web Filter, and App Control details successfully fetched and saved.")
        return combined_details, x_list, adresses, services_tab, web_filter_profiles, app_control_profiles

    else:
        log_and_print("Failed to fetch VLAN, Firewall, Web Filter, or App Control details.")
        return None, None, None, None, None, None


if __name__ == "__main__":
    main_controller()
