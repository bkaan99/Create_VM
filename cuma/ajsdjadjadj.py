import os
import shutil

def copy_and_rename_files(source_folder, target_folder, prefix):
    try:
        # Kaynak dizini kontrol et
        if not os.path.exists(source_folder):
            print(f"Kaynak dizin bulunamadı: {source_folder}")
            return

        # Hedef dizini kontrol et ve oluştur
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Kaynak dizinindeki dosyaları kopyala ve isimlerini değiştir
        for filename in os.listdir(source_folder):
            source_file_path = os.path.join(source_folder, filename)
            target_file_path = os.path.join(target_folder, f"{prefix}_{filename}")

            shutil.copy2(source_file_path, target_file_path)
            print(f"{filename} dosyası başarıyla kopyalandı ve ismi değiştirildi.")

    except Exception as e:
        print(f"Hata: {e}")

def main():
    # Kaynak ve hedef dizinleri belirle
    source_folder = "/vmfs/volumes/Datastore01/bkaan_deneme/"
    target_folder = "/vmfs/volumes/Datastore01/bkaan_deneme_clone/"
    prefix = "clone"

    # Dosyaları kopyala ve isimlerini değiştir
    copy_and_rename_files(source_folder, target_folder, prefix)

if __name__ == "__main__":
    main()
