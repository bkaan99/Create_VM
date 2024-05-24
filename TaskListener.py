from pyVim.connect import  Disconnect
from vCenter.IaaS.Connections.vSphere_connection import create_vsphere_connection


def list_tasks(content):
    tasks_info_list = []
    recent_tasks = content.taskManager.recentTask
    for task in recent_tasks:
        info = task.info
        try:
            entity_name = getattr(info, 'entityName', None)
            if entity_name:
                task_info = {
                    "Task": getattr(info, 'name', 'N/A'),
                    "Entity Name": entity_name,
                    "Cancelable": getattr(info, 'cancelable', 'N/A'),
                    "Cancelled": getattr(info, 'cancelled', 'N/A'),
                    "Change Tag": getattr(info, 'changeTag', 'N/A'),
                    "Complete Time": getattr(info, 'completeTime', 'N/A'),
                    "Description": getattr(info, 'description', 'N/A') if isinstance(getattr(info, 'description', 'N/A'), str) else getattr(getattr(info, 'description', None), 'message', 'N/A'),
                    "Description ID": getattr(info, 'descriptionId', 'N/A'),
                    "Error Message": getattr(info.error, 'msg', 'No error message') if info.error else 'No error message',
                    "Task Key": getattr(info, 'key', 'N/A'),
                    "Progress": getattr(info, 'progress', 'N/A'),
                    "Queue Time": getattr(info, 'queueTime', 'N/A'),
                    "Start Time": getattr(info, 'startTime', 'N/A'),
                    "State": getattr(info, 'state', 'N/A'),
                }
                tasks_info_list.append(task_info)
        except AttributeError as e:
            print(f"An error occurred: {e}")

    return tasks_info_list

def main():
    vCenter_host_ip = "10.14.45.10"
    vCenter_user = "administrator@vsphere.local"
    vCenter_password = "Aa112233!"

    si, content = create_vsphere_connection(vCenter_host_ip, vCenter_user, vCenter_password)

    list_tasks(content)

    Disconnect(si)

if __name__ == "__main__":
    main()
