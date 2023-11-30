from bs4 import BeautifulSoup
import requests

base_url = "https://classic.hinnavaatlus.ee/products/Mobiiltelefonid/Mobiiltelefonid/?sort=min_price&page={}"

start_page = 1
max_page = 41

with open("phone_details.txt", "w", encoding="utf-8") as file:
    for page_number in range(start_page, max_page + 1):
        url = base_url.format(page_number)
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')

        product_items = soup.find_all('li', class_='product-list-item')

        for item in product_items:
            price_element = item.find('span', class_='product-list-current-price')

            if price_element:
                price = price_element.get_text(strip=True)
                price_cleaned = price.replace('€', '').replace('\xa0', '').replace(',', '.')
                file.write(f"{price_cleaned}\n")
