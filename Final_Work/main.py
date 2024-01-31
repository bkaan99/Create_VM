from Final_Work import copyfile
from Final_Work import main
from Final_Work import registry_vm


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
