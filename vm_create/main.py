import libvirt
import sys
from tqdm import tqdm
import time

def establish_connection():
    try:
        conn = libvirt.open('qemu:///system')
        if conn is None:
            print('Hypervisor ile bağlantı kurulamadı.')
            sys.exit(1)
        return conn
    except libvirt.libvirtError as e:
        print(f'Hata: {e}')
        sys.exit(1)


def get_vm_properties():
    try:
        vm_name = input('Sanal makine adını girin: ')
        memory = int(input('Bellek miktarını (KiB cinsinden) girin: '))
        vcpu = int(input('vCPU sayısını girin: '))
        disk_size = int(input('Disk boyutunu (GiB cinsinden) girin: '))
        supported_os_types = ['linux', 'windows', 'ubuntu']  # Desteklenen işletim sistemleri listesi
        os_type = input('İşletim sistemi türünü girin (varsayılan: linux): ') or 'linux'

        if os_type.lower() not in supported_os_types:
            print('Hata: Geçersiz işletim sistemi tipi.')
            sys.exit(1)

        iso_path = input('ISO dosyasının yolunu girin (opsiyonel): ')

        return vm_name, memory, vcpu, disk_size, os_type, iso_path

    except ValueError as ve:
        print(f'Hata: Geçersiz değer. {ve}')
        sys.exit(1)


def create_vm(conn, vm_name, memory, vcpu, disk_size, os_type='linux', iso_path=None):
    try:
        os_info = f"""
                    <os>
                        <type arch='x86_64' machine='pc-i440fx-2.12'>{os_type}</type>
                        <boot dev='hd'/>
                    </os>
                """

        xml_desc = f"""
            <domain type='kvm'>
                <name>{vm_name}</name>
                <memory unit='KiB'>{memory}</memory>
                <vcpu placement='static'>{vcpu}</vcpu>
                <os>
                    <type arch='x86_64' machine='pc-i440fx-2.12'>{os_type}</type>
                    <boot dev='hd'/>
                </os>
                {os_info}  <!-- Eklenen kısım -->
                <devices>
                    <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='{vm_name}.qcow2'/>
                        <target dev='vda' bus='virtio'/>
                        <size unit='GiB'>{disk_size}</size>
                    </disk>
                    <disk type='file' device='cdrom' optional='yes'>
                        <driver name='qemu' type='raw'/>
                        <source file='{iso_path}'/>
                        <target dev='hda' bus='ide'/>
                        <readonly/>
                    </disk>
                    <interface type='network'>
                        <mac address='52:54:00:11:22:33'/>
                        <source network='default'/>
                        <model type='virtio'/>
                    </interface>
                </devices>
            </domain>
        """

        with tqdm(total=100, desc=f'Sanal makine {vm_name} oluşturuluyor',
                  bar_format='{desc}: {percentage:3.0f}%|{bar:50}|') as pbar:
            domain = conn.createXML(xml_desc, 0)
            for _ in range(100):
                time.sleep(0.1)  # Simülasyon amacıyla bir bekleme ekledik.
                pbar.update(1)

        if domain is None:
            print('Sanal makine oluşturulamadı.')
            sys.exit(1)

        print(f'Sanal makine {vm_name} oluşturuldu.')

    except libvirt.libvirtError as e:
        print(f'Hata: {e}')
        sys.exit(1)


def list_created_vms(conn):
    try:
        domains = conn.listDomainsID()
        if not domains:
            print('Oluşturulmuş sanal makine bulunamadı.')
        else:
            print('Oluşturulmuş Sanal Makineler:')
            for domain_id in domains:
                domain = conn.lookupByID(domain_id)
                print(f'ID: {domain_id}, Adı: {domain.name()}')
    except libvirt.libvirtError as e:
        print(f'Hata: {e}')
        sys.exit(1)

def destroy_vm(conn, vm_name):
    try:
        domain = conn.lookupByName(vm_name)
        if domain is not None:
            domain.destroy()
            print(f'Sanal makine {vm_name} durduruldu.')
        else:
            print(f'Sanal makine {vm_name} bulunamadı.')
    except libvirt.libvirtError as e:
        print(f'Hata: {e}')
        sys.exit(1)

# def show_vm_details(conn, vm_name):
#     try:
#         domain = conn.lookupByName(vm_name)
#         if domain is None:
#             print(f'Sanal makine {vm_name} bulunamadı.')
#             sys.exit(0)
#
#         print(f'\nSanal Makine Detayları ({vm_name}):')
#         print('-----------------------------------')
#         print(f'ID: {domain.ID()}')
#         print(f'UUID: {domain.UUIDString()}')
#         print(f'Versiyon: {domain.version()}')
#         print(f'VCPUs: {domain.maxVcpus()}')
#         print(f'Bellek Miktarı: {domain.maxMemory()} KiB')
#         print(f'VirtIO Arabirim Sayısı: {len(domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0))}')
#         print(f'Disk Sayısı: {len(domain.listDevices('disk'))}')
#         print(f'Aktif: {"Evet" if domain.isActive() else "Hayır"}')
#         print(f'Durum: {libvirt.virDomainState(domain.state()[0])}')
#
#     except libvirt.libvirtError as e:
#         print(f'Hata: {e}')
#         sys.exit(1)


if __name__ == "__main__":
    conn = establish_connection()
    is_running = True

    while is_running:
        print('\nHangi işlem yapmak istiyorsunuz?')
        print('1- VM oluşturma')
        print('2- VM Listesini görme')
        print('3- VM detaylarını öğrenme')
        print('4- VM\'leri silme')
        print('5- Çıkış')

        choice = input('Seçiminizi yapın (1-5): ')

        if choice == '1':
            vm_name, memory, vcpu, disk_size, os_type, iso_path = get_vm_properties()
            create_vm(conn, vm_name, memory, vcpu, disk_size, os_type, iso_path)
        elif choice == '2':
            list_created_vms(conn)
        elif choice == '3':
            vm_name = input('Bilgilerini görmek istediğiniz sanal makinenin adını girin: ')
            #show_vm_details(conn, vm_name)
        elif choice == '4':
            vm_name = input('Silmek istediğiniz sanal makinenin adını girin: ')
            destroy_vm(conn, vm_name)
        elif choice == '5':
            break
        else:
            print('Geçersiz seçim.')