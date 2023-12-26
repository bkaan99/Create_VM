from Son import copyfile
from Son import main
from Son import rename_vm
from Son import datastore_file_renamer
from Son import powerOn
from Son import registry_vm
from Son import shut_down
from Son import destroy_vm


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
