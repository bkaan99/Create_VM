from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vm_by_name(content, vm_name):
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in vm_view.view:
        if vm.name == vm_name:
            return vm
    return None

def wait_for_task(task):
    """Waits and provides updates on a vSphere task until it is completed."""
    task_done = False
    while not task_done:
        if task.info.state == vim.TaskInfo.State.success:
            print("Task completed successfully.")
            task_done = True
        elif task.info.state == vim.TaskInfo.State.error:
            print(f"Error: {task.info.error}")
            task_done = True

def get_vm_question(vm):
    """
    Gets the questions and answers for a virtual machine.
    """
    if not isinstance(vm, vim.VirtualMachine):
        raise ValueError("Invalid virtual machine object.")

    question_answers = []
    for question in vm.config.extraConfig:
        question_id = question.key
        answer_value = question.value
        question_answers.append({"question_id": question_id, "answer_value": answer_value})

    return question_answers


def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    source_vm_name = "esxi_centos_pzt"

    source_vm = get_vm_by_name(content, source_vm_name)

    if source_vm is None:
        print(f"VM {source_vm_name} not found.")
        Disconnect(service_instance)
        return

    question_id = "your_question_id"
    answer_value = "your_answer_value"

    deneme = get_vm_question(source_vm)

    try:
        # AnswerVM metodunu kullanarak soruya yanıt verme
        task = source_vm.AnswerVM(id=question_id, answer=answer_value)
        wait_for_task(task)
    except Exception as e:
        print(f"Error answering VM question: {e}")

    Disconnect(service_instance)

if __name__ == "__main__":
    main()
