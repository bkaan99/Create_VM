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


def answer_vm_question(vm):
    if vm.runtime.question is not None:
        question_id = vm.runtime.question.id
        question_text = vm.runtime.question.text

        for choice_info in vm.runtime.question.choice.choiceInfo:
            if choice_info.summary == "I Copied It":
                choice_id = choice_info.key

                # Örnek bir yanıt oluşturun
                answer = vim.vm.AnswerVM(questionId=question_id, choiceId=choice_id)

                # Sanal makineyi yeniden yapılandırma görevini başlatın
                reconfig_task = vm.ReconfigVM_Task(spec=vim.vm.ConfigSpec(answer=answer))

                # Görevin tamamlanmasını bekleyin
                wait_for_task(reconfig_task)
                break
    else:
        print("Answer not found for question")

def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    service_instance = SmartConnect(host="10.14.45.11",
                                    user="root",
                                    pwd="Aa112233!",
                                    sslContext=ssl_context)

    content = service_instance.RetrieveContent()

    source_vm_name = "11"

    source_vm = get_vm_by_name(content, source_vm_name)

    if source_vm is None:
        print(f"VM {source_vm_name} not found.")
        Disconnect(service_instance)
        return

    if source_vm:
        answer_text = "This virtual machine might have been moved or copied. In order to configure certain management and networking features, VMware ESX needs to know if this virtual machine was moved or copied. If you don't know, answer 'I Copied It'."
        # power on the VM
        if source_vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            task = source_vm.PowerOnVM_Task()
            wait_for_task(task)

        try:
            answer_vm_question(source_vm)
        except Exception as e:
            print(f"Error: {e}")


    Disconnect(service_instance)

if __name__ == "__main__":
    main()
