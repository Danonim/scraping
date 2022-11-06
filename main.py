import requests
from os import mkdir
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

def main():

    laptops_url_list = []
    for i in range(1, 68):
        url = f'https://rozetka.com.ua/ua/notebooks/c80004/page={i}/'

        req = requests.get(url=url, headers=headers)
        result = req.content

        soup = BeautifulSoup(result, 'lxml')
        laptops = soup.find_all(class_="goods-tile__picture ng-star-inserted")

        for laptop in laptops:
            laptop_page_url = laptop.get('href')
            laptops_url_list.append(laptop_page_url)

    id = 0
    for url in laptops_url_list:
        req = requests.get(url=url, headers=headers)
        result = req.content

        soup = BeautifulSoup(result, 'lxml')

        laptop_image_url = soup.find(class_="picture-container__picture")
        img_url = laptop_image_url.get('src')
        q = requests.get(url=img_url, headers=headers)
        laptop_image = q.content

        try:
            price = soup.find(class_="product-prices__inner ng-star-inserted").text
        except AttributeError:
            price = "Цей ноутбук безцінний!"

        try:
            fullname = soup.find(class_="product__title").text.strip().split("/", 1)
            fullname.append(" ")
        except AttributeError:
            fullname = ["Назви немає", ":("]

        try:
            description = soup.find(
                class_="product-about__description-content text product-about__description-content_state_collapsed").text
        except AttributeError:
            description = "Опису немає"

        name = fullname[0].replace('"', '').replace('|', ',').replace('\\', ',').replace(':', ';').replace('*', 'x')
        id += 1
        mkdir(f"Laptops/{name}({id})")

        try:
            with open(f'Laptops/{name}({id})/description.txt', 'w', encoding='utf-8') as file:
                file.write(f"Ціна: {price}\nОпис {fullname[0]} {fullname[1]} {description}")

            with open(f'Laptops/{name}({id})/img.jpg', 'wb') as f:
                f.write(laptop_image)
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    main()
