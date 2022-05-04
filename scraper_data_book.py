""" Descriription of this script 
Scraping data from an url of one book on this website : 
https://books.toscrape.com/index.html 
"""

import csv

from bs4 import BeautifulSoup
import requests


# Get url of a book
url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
reponse = requests.get(url)
page = reponse.content

# Parse the url
soup = BeautifulSoup(page, "html.parser")

# Get all data of the book
title = soup.find("h1").string

all_td = soup.find_all("td")
list_all_td = []
for td in all_td :
	list_all_td.append(td.string)
upc = list_all_td[0]
price_incl_tax = list_all_td[2]
price_excl_tax = list_all_td[3]
number_available = list_all_td[5]

img_url = soup.find("img")["src"].replace("../../", "http://books.toscrape.com/")

category = soup.find_all("a")[3].string

product_description = soup.find_all("p")[3].string

review_rating = soup.find_all("p", class_="star-rating")[0].get("class")[1]
rating_dict = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
rating = rating_dict[review_rating] + "/5"

# Write all data in csv file
fieldnames = [
    "product page url",
    "upc",
    "title",
    "price including tax",
    "price excluding tax",
    "number available",
    "product description",
    "category",
    "review rating",
    "image url",
]
data_book = [
    url,
    upc,
    title,
    price_incl_tax,
    price_excl_tax,
    number_available,
    product_description,
    category,
    rating,
    img_url,
]
with open("data_book.csv", "w") as file_csv:
    writer = csv.DictWriter(file_csv, delimiter=";", fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(
        {
            "product page url": url,
            "upc": upc,
            "title": title,
            "price including tax": price_incl_tax,
            "price excluding tax": price_excl_tax,
            "number available": number_available,
            "product description": product_description,
            "category": category,
            "review rating": rating,
            "image url": img_url,
        }
    )