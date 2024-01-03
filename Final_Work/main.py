from Final_Work import copyfile
from Final_Work import main
from Final_Work import rename_vm
from Final_Work import datastore_file_renamer
from Final_Work import powerOn
from Final_Work import registry_vm
from Final_Work import shut_down
from Final_Work import destroy_vm


def main():
    print("Vm Oluşturma İşlemi Başladı")

    copyfile.main()
    if copyfile.main() == 0:
        print("VM kopyalama işlemi başarılı")
        registry_vm.main()

        print("VM kayıt işlemi başarılı")


    else:
        print("VM kopyalama işlemi başarısız")


if __name__ == "__main__":
    main()
