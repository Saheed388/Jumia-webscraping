from bs4 import BeautifulSoup
import requests
import pandas as pd
from google.cloud import storage

base_url = "https://www.jumia.com.ng/computing/?page="

data = []
page_number = 1

while True:
    url = base_url + str(page_number)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_list = soup.find_all("a", class_="core")

    if len(product_list) == 0:
        break

    for product in product_list:
        name_elem = product.find("h3", class_="name")
        if name_elem:
            name = name_elem.text
        else:
            name = "N/A"

        price_elem = product.find("div", class_="prc")
        if price_elem:
            price = price_elem.text
        else:
            price = "N/A"

        old_price_elem = product.find("div", class_="old")
        if old_price_elem:
            old_price = old_price_elem.text
        else:
            old_price = "N/A"

        discount_elem = product.find("div", class_="bdg _dsct _sm")
        if discount_elem:
            discount = discount_elem.text
        else:
            discount = "N/A"

        data.append({"Name": name, "Price": price, "Old Price": old_price, "Discount": discount})

    page_number += 1

df = pd.DataFrame(data)
df.to_csv("product_data.csv", index=False)

# Upload CSV file to Google Cloud Storage bucket
storage_client = storage.Client.from_service_account_json ('alt-school-project-386517-fcb14f08a9df.json')
bucket_name = "saeed-altschool-bucket"  # Replace with your bucket name
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob("product_data.csv")
blob.upload_from_filename("product_data.csv")




from bs4 import BeautifulSoup
import requests
import pandas as pd
from google.cloud import storage
import schedule
import time

def scrape_and_upload_data():
    base_url = "https://www.jumia.com.ng/computing/?page="
    data = []
    page_number = 1

    while True:
        url = base_url + str(page_number)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        product_list = soup.find_all("a", class_="core")

        if len(product_list) == 0:
            break

        for product in product_list:
            name_elem = product.find("h3", class_="name")
            if name_elem:
                name = name_elem.text
            else:
                name = "N/A"

            price_elem = product.find("div", class_="prc")
            if price_elem:
                price = price_elem.text
            else:
                price = "N/A"

            old_price_elem = product.find("div", class_="old")
            if old_price_elem:
                old_price = old_price_elem.text
            else:
                old_price = "N/A"

            discount_elem = product.find("div", class_="bdg _dsct _sm")
            if discount_elem:
                discount = discount_elem.text
            else:
                discount = "N/A"

            data.append({"Name": name, "Price": price, "Old Price": old_price, "Discount": discount})

        page_number += 1

    df = pd.DataFrame(data)
    df.to_csv("product_data.csv", index=False)

    # Upload CSV file to Google Cloud Storage bucket
    storage_client = storage.Client.from_service_account_json('alt-school-project-386517-fcb14f08a9df.json')
    bucket_name = "saeed-altschool-bucket"  # Replace with your bucket name
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("product_data.csv")
    blob.upload_from_filename("product_data.csv")

# Schedule the script to run every weekend (Saturday)
schedule.every().saturday.do(scrape_and_upload_data)

while True:
    schedule.run_pending()
    time.sleep(1)
