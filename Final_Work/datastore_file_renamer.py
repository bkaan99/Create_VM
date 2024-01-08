from Final_Work.esxi_connection import *

def rename_files_in_folder(folder, content, datacenter, old_name, new_name):
    try:
        # FileManager'ı al
        file_manager = content.fileManager

        # Klasör içindeki dosyanın eski ve yeni yollarını belirle
        source_file_path = f"[{datacenter.name}] {folder}/{old_name}"
        target_file_path = f"[{datacenter.name}] {folder}/{new_name}"

        # Datacenter nesnesini al
        datacenter_obj = None
        for child in content.rootFolder.childEntity:
            if isinstance(child, vim.Datacenter):
                datacenter_obj = child
                break

        if datacenter_obj is None:
            print("Datacenter bulunamadı.")
            return

        # Dosyayı kopyala
        file_manager.CopyFile(sourceName=source_file_path, sourceDatacenter=datacenter_obj,
                              destinationName=target_file_path, destinationDatacenter=datacenter_obj)


        print(f"Dosya başarıyla kopyalandı: {target_file_path}")


       # kopyalanan dosyayı sil
        file_manager.DeleteFile(name=source_file_path, datacenter=datacenter_obj)


        print(f"Dosya başarıyla silindi: {source_file_path}")
    except Exception as e:
        print(f"Hata: {e}")

def find_file_in_folder(ds):
    search = vim.HostDatastoreBrowserSearchSpec()
    search.matchPattern = "*.vmx"
    search_ds = ds.browser.SearchDatastoreSubFolders_Task(datastorePath="[%s]" % ds.name, searchSpec=search)
    while search_ds.info.state != "success":
        print(search_ds.info.state)
        print(search_ds.info.error.msg)
        pass
    results = search_ds.info.result
    target_folder = "esxi_centos_pzt"  # Adjust the folder path as needed

    for result in results:
        # Adjust the comparison to consider the datastore name in the folderPath
        if f"[{ds.name}] {target_folder}" in result.folderPath:
            print("Found file:", result.folderPath)
            for f in result.file:
                if f.path.endswith(".vmx"):
                    print("Found file:", f.path)
                    return f.path
                else:
                    print("File not found.")
                    return None
        else:
            print("File not found.")

    return None

def main(Copying_vm_name,Copied_folder_name, esxi_host_ip, esxi_user, esxi_password):

    service_instance, content = create_vsphere_connection(esxi_host_ip, esxi_user, esxi_password)

    source_vm_name = Copying_vm_name

    source_vm = get_vm_by_name(content, source_vm_name)

    datastoreFile = {"nvram","vmdk","vmsd","vmxf","vmx","log"}

    finded_files = find_file_in_folder(source_vm.datastore[0])


    if source_vm is not None:
        for i in datastoreFile:
            folder_name = Copied_folder_name
            file_to_rename = "new_bkaan_deneme"+"."+i  # Specify the file to be renamed
            new_file_name = "bkaan_centos"+"."+i  # Specify the new file name

            rename_files_in_folder(folder_name, content, source_vm.datastore[0], file_to_rename, new_file_name)
    else:
        print("VM bulunamadı.")

if __name__ == "__main__":
    main()
