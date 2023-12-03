from bs4 import BeautifulSoup
import requests

url = "https://www.mobiletrade.ee/en/c/phones#/page/1"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

phone_items = soup.find_all('div', class_='catalog-taxons-product catalog-taxons-product--grid-view')

phone_details_list = []

for item in phone_items:
    phone_link = item.find('div', class_='catalog-taxons-product catalog-taxons-product--grid-view').find('a')['href']
    phone_page = requests.get(phone_link)
    phone_soup = BeautifulSoup(phone_page.content, 'html.parser')

    attribute_divs = phone_soup.find('table', id='info-table').find_all('table')
    phone_details = {}
    for div in attribute_divs:
        attributes = div.find_all('tr')
        for attribute in attributes:
            key = attribute.find('td').text.strip()
            value = attribute.find('td').find_next('td').text.strip()
            phone_details[key] = value

    phone_details_list.append(phone_details)

unique_keys = set()
for phone_details in phone_details_list:
    unique_keys.update(phone_details.keys())

with open("phone_attributes.txt", "w", encoding="utf-8") as file:
    file.write(",".join(unique_keys) + "\n")

    for phone_details in phone_details_list:
        row_values = [phone_details.get(key, "") for key in unique_keys]
        file.write(",".join(row_values) + "\n")
