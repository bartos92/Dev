import requests
from bs4 import BeautifulSoup
import json

url = "https://auto.ria.com/uk/legkovie/bmw/state/ternopol/?page=1"

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

# with open("index.html",encoding="utf-8") as file:
#     src = file.read()

soup = BeautifulSoup(src, "lxml")


def get_all_golf():
    all_golf = soup.find_all(class_="content")

    all_golf_dict = {}

    for item in all_golf:
        item_text = item.find(class_="head-ticket").text
        item_url = item.find(class_="address").get("href")
        item_price = item.find(class_="price-ticket").text
        item_location = item.find(class_="item-char view-location js-location").text
        item_location = item_location[:-8]
        golf_id = item_url.split("_")[-1]
        golf_id = golf_id[:-5]

        all_golf_dict[golf_id] = {
            "Title": item_text,
            "Price": item_price,
            "Url": item_url,
            "Location": item_location
        }

    with open("all_golf_dict.json","w") as file:
        json.dump(all_golf_dict, file, indent=4, ensure_ascii=False)


new_golf = {}


def check_new_golf():
    with open("all_golf_dict.json") as file:
        all_golf_dict = json.load(file)

    # with open("index.html", encoding="utf-8") as file:
    #     src = file.read()

    url = "https://auto.ria.com/uk/legkovie/bmw/state/ternopol/?page=1"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    all_golf = soup.find_all(class_="content")

    for item in all_golf:
        item_url = item.find(class_="address").get("href")
        golf_id = item_url.split("_")[-1]
        golf_id = golf_id[:-5]

        if golf_id in all_golf_dict:
            continue
        else:
            item_text = item.find(class_="head-ticket").text
            item_price = item.find(class_="price-ticket").text
            item_location = item.find(class_="item-char view-location js-location").text
            item_location = item_location[:-8]
            all_golf_dict[golf_id] = {
                "Title": item_text,
                "Price": item_price,
                "Url": item_url,
                "Location": item_location
            }

            new_golf[golf_id] = {
                 "Title": item_text,
                 "Price": item_price,
                 "Url": item_url,
                 "Location": item_location
            }

    with open("all_golf_dict.json","w") as file:
        json.dump(all_golf_dict, file, indent=4, ensure_ascii=False)

    return new_golf


def main():
    # get_all_golf()
    print(check_new_golf())


if __name__ == "__main__":
    main()