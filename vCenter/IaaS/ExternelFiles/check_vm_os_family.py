def main(os_family, os_version):

    if "Windows" in os_family:
        if "Windows Server 2016" in os_version:
            template_name = "bkaan_windows_template"
            print("Windows işletim sistemi için VM Template'i seçildi.")
            return template_name

        if "Windows 2018" in os_version:
            template_name = "bkaan_windows_template"
            print("Windows işletim sistemi için VM Template'i seçildi.")
            return template_name

        else:
            template_name = "New_Windows_VM"
            return template_name

    elif "Linux" in os_family:
        if "SUSE" in os_version:
            template_name = "SUSE-Temp-15-3"
            print("Linux işletim sistemi için VM Template'i seçildi.")
            return template_name

        if "Ubuntu" in os_version:
            template_name = "Ubuntu_Deneme"
            print("Linux işletim sistemi için VM Template'i seçildi.")
            return template_name

    elif os_family == "Other":
        pass

    elif os_family == "MacOS":
        pass

    else:
        print("OS family not found")
