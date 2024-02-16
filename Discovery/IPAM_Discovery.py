import requests
from bs4 import BeautifulSoup


def update_session(session):
    # Oturum bilgilerini burada güncelle
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'phpipam=7vtnj6q4aho4qkaikog6hdjcm5; table-page-size=50',
        'Host': '172.28.0.27',
        'Pragma': 'no-cache',
        'Referer': 'https://172.28.0.27/index.php?page=tools&section=subnets',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    session.headers.update(headers)

def extract_customer_names(html_content):
    # HTML içeriğini parse et
    soup = BeautifulSoup(html_content, 'html.parser')

    customers_table = soup.findAll('table')
    # Table id si customers olan tabloyu bul
    for table in customers_table:
        if table.get('id') == 'customers':
            # Tablodaki tüm satırları bul
            customer_rows = table.find_all('tr')
            # Müşteri isimlerini saklayacak bir liste oluştur
            customer_names = []
            # Her müşteri satırını döngüye alarak isimleri çıkar
            for row in customer_rows:
                # İlk hücreyi bul (müşteri adı burada)
                cell = row.find('td')
                if cell:
                    # İlk hücredeki metni al (müşteri adı veya diğer veri)
                    cell_text = cell.text.strip()
                    # Eğer hücre metni boş değilse (müşteri adı varsa)
                    if cell_text:
                        # Müşteri adını listeye ekle
                        customer_names.append(cell_text)
            return customer_names

    else:
        return []


def is_customer(text):
    # Metin içerisinde 'phpIPAM' ve 'SubnetCustomers' geçiyorsa bu bir müşteri değil
    return 'phpIPAM' not in text and 'SubnetCustomers' not in text



def main():
    url = 'https://172.28.0.27/index.php?page=tools&section=customers'

    # Oturum oluştur
    session = requests.Session()

    # Oturum bilgilerini güncelle
    update_session(session)

    try:
        response = session.get(url, verify=False)
        if response.status_code == 200:
            customer_names = extract_customer_names(response.text)
            print("Müşteri İsimleri:")
            # Müşteri isimlerini yazdır
            for index, name in enumerate(customer_names):
                if is_customer(name):
                    print(f"{index:02d} = {name}")
        else:
            print("İstek başarısız oldu. Durum kodu:", response.status_code)
    except Exception as e:
        print("Bir hata oluştu:", str(e))


if __name__ == "__main__":
    main()
