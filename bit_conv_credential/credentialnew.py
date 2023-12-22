from PIL import Image
import os

def find_desktop_path():
    # İşletim sistemini kontrol et
    if os.name == 'posix':  # Linux
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    elif os.name == 'nt':   # Windows
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    elif os.name == 'mac':  # MacOS
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        raise OSError("Unsupported operating system")

def convert_to_32bit(input_filename, output_filename, input_folder, output_folder):
    # Resmi aç
    input_path = os.path.join(input_folder, input_filename)
    image = Image.open(input_path)

    # Renk derinliğini 32 bit olarak değiştir
    image = image.convert("RGBA")

    # Yeni 32 bit resmi kaydet
    desktop_path = find_desktop_path()
    output_path = os.path.join(desktop_path, output_folder, output_filename)
    image.save(output_path, "BMP")

# Kullanım örneği
input_file = "output2.bmp"
output_file = "output32bit.bmp"
input_folder = r"C:\Windows\System32"
output_folder = find_desktop_path()

convert_to_32bit(input_file, output_file, input_folder, output_folder)
