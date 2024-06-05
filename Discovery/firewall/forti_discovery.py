from datetime import datetime
import pandas as pd
from Discovery.firewall.utils_fortinet import main_controller


def append_dataframe_given_values(key, value, is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes):
    dataFrameForInsert.loc[len(dataFrameForInsert)]=[str(key),str(value), is_deleted, version, created_date, vm_id, virtualization_environment_type,virtualization_environment_ip, nodeName, notes]


def combined_details_to_dataframe(combined_details):

    for detail in combined_details:
        for key, value in detail.items():
            if isinstance(value, list):
                for item in value:
                    for key2, value2 in item.items():
                        append_dataframe_given_values(key2, value2, isDeletedValueForAppend, versionForAppend, createdDateForAppend, str(detail['VLAN ID']), virtualizationEnvironmentType, virtualalizationEnvironmentIp, f"VLAN/{key}", "/api/v2/cmdb/system/interface")
            else:
                append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, str(detail['VLAN ID']), virtualizationEnvironmentType, virtualalizationEnvironmentIp, "VLAN", "/api/v2/cmdb/system/interface")

def firewall_rules_to_dataframe(firewall_rules):
    for rule in firewall_rules:
        for key, value in rule.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, rule['policyid'], virtualizationEnvironmentType, virtualalizationEnvironmentIp, "Firewall", "/api/v2/cmdb/firewall/policy")


def adresses_to_dataframe(adresses):
    for index,adress in enumerate(adresses):
        for key, value in adress.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "Adresses", f"/api/v2/cmdb/firewall/address/{index}")

def services_tab_to_dataframe(services_tab):
    for index,service in enumerate(services_tab):
        for key, value in service.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "Services", f"/api/v2/cmdb/firewall.service/custom/{index}")

def web_filter_profiles_to_dataframe(web_filter_profiles):
    for index,profile in enumerate(web_filter_profiles):
        for key, value in profile.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "Web Filter Profiles", f"/api/v2/cmdb/webfilter/profile/{index}")


def app_control_profiles_to_dataframe(app_control_profiles):
    for index,profile in enumerate(app_control_profiles):
        for key, value in profile.items():
            append_dataframe_given_values(key, value, isDeletedValueForAppend, versionForAppend, createdDateForAppend, None, virtualizationEnvironmentType, virtualalizationEnvironmentIp, "App Control Profiles", f"/api/v2/cmdb/application/control/profile/{index}")

def controller_method():
    (combined_details,
     firewall_rules,
     adresses,
     services_tab,
     web_filter_profiles,
     app_control_profiles) = main_controller()

    combined_details_to_dataframe(combined_details)
    print("combined_details_to_dataframe tamamlandı")
    firewall_rules_to_dataframe(firewall_rules)
    print("firewall_rules_to_dataframe tamamlandı")
    adresses_to_dataframe(adresses)
    print("adresses_to_dataframe tamamlandı")
    services_tab_to_dataframe(services_tab)
    print("services_tab_to_dataframe tamamlandı")
    web_filter_profiles_to_dataframe(web_filter_profiles)
    print("web_filter_profiles_to_dataframe tamamlandı")
    app_control_profiles_to_dataframe(app_control_profiles)
    print("app_control_profiles_to_dataframe tamamlandı")


if __name__ == "__main__":
    createdDateForAppend = datetime.now()
    versionForAppend = 1
    isDeletedValueForAppend = False
    virtualizationEnvironmentType = "Fortinet"
    virtualalizationEnvironmentIp = "10.14.26.1"

    dataFrameColumns = ["key","value","is_deleted","version","created_date","vm_id","virtualization_environment_type","virtualization_environment_ip","node","notes"]
    dataFrameForInsert = pd.DataFrame(columns=dataFrameColumns)
    # engineForPostgres = create_engine('postgresql+psycopg2://postgres:Cekino.123!@10.14.45.69:7100/karcin_pfms')
    #
    # connectionForPostgres = psycopg2.connect(
    #     host="10.14.45.69",
    #     port="7100",
    #     database="karcin_pfms",
    #     user="postgres",
    #     password="Cekino.123!")
    # cursorForPostgres = connectionForPostgres.cursor()

    controller_method()

    dataFrameForInsert.to_csv("forti_disc.csv", index=False)