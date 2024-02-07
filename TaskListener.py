from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import time

def list_tasks(content):

    for task in content.taskManager.recentTask:
        try:
            if task.info.entityName:
                print(f"Task: {task.info.descriptionId} | Entity: {task.info.entityName} | State: {task.info.state}")

        except Exception as e:
            print(f"Error: {e}")

def main():
    # ESXi host details
    esxi_host = "10.14.45.11"
    esxi_user = "root"
    esxi_password = "Aa112233!"

    # Disable SSL certificate verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Connect to ESXi host
    si = SmartConnect(
        host=esxi_host,
        user=esxi_user,
        pwd=esxi_password,
        sslContext=ssl_context,
    )

    # Retrieve content
    content = si.RetrieveContent()

    # List tasks running on the ESXi host
    list_tasks(content)

    # Disconnect from ESXi host
    Disconnect(si)

if __name__ == "__main__":
    main()
