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
    soup = BeautifulSoup(html_content, 'html.parser')

    customers_table = soup.findAll('table')
    for table in customers_table:
        if table.get('id') == 'customers':
            customer_rows = table.find_all('tr')
            customer_names = []
            for row in customer_rows:
                cell = row.find('td')
                if cell:
                    cell_text = cell.text.strip()
                    if cell_text:
                        customer_names.append(cell_text)
            return customer_names

    else:
        return []


def extract_subnets(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    subnets_table = soup.findAll('table')

    for table in subnets_table:
        if table.get('id') == 'subnetsMenu':
            subnet_rows = table.find_all('td')

            for row in subnet_rows:
                if row.get('id') == 'subnetsLeft':
                    #find div class 'subnets'
                    subnets = row.find_all('div', class_='subnets')

                    Available_subnets = subnets[0]
                    Associated_VLANs = subnets[1]

                    Subnet_Folders_List = folder_names(Available_subnets)


                    #Subnet_Folders_List içerisinde str değerlerin içinde sayı olan verileri kaldır
                    Subnet_Folders_List_Names = [x for x in Subnet_Folders_List if not any(c.isdigit() for c in x)]

                    print(Subnet_Folders_List_Names)

                    # for li in Available_subnets_tab1.find_all('li'):
                    #     print(li.text)
                    #


                    # for folders in Available_subnets.find_all('a'):
                    #     #folders içerisinde bulunan a etiketlerinin text'lerini al
                    #
                    #     if folders.text:
                    #         print(folders.text)


    else:
        return []


def folder_names(Available_subnets):

    Available_subnets_tab1 = Available_subnets.find('ul')

    # Available_subnets_tab1 içerisindeki her bir ul etiketini tek tek sil
    for ul in Available_subnets_tab1.find_all('ul'):
        ul.decompose()


    for div in Available_subnets_tab1:
        div_text = div.text
        div_text = div_text.split('\n')
        div_text = [x for x in div_text if x]




    return div_text

def main():

    url_customers = 'https://172.28.0.27/index.php?page=tools&section=customers'
    url_subnets = 'https://172.28.0.27/index.php?page=subnets&section=1'

    # Oturum oluştur
    session = requests.Session()

    # Oturum bilgilerini güncelle
    update_session(session)

    try:
        response = session.get(url_customers, verify=False)
        if response.status_code == 200:

            #Customer Names
            customer_names = extract_customer_names(response.text)
            print("Müşteri İsimleri:")
            for index, name in enumerate(customer_names):
                print(f"{index:02d} = {name}")

        else:
            print("İstek başarısız oldu. Durum kodu:", response.status_code)
    except Exception as e:
        print("Bir hata oluştu:", str(e))


    try:
        response = session.get(url_subnets, verify=False)
        if response.status_code == 200:
            #Subnets
            print("Subnetler:")
            subnets = extract_subnets(response.text)


        else:
            print("İstek başarısız oldu. Durum kodu:", response.status_code)

    except Exception as e:
        print("Bir hata oluştu:", str(e))



if __name__ == "__main__":
    main()
