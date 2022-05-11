'''
Script Description:
Extract all data of all books in a category
to write them to a csv file.
Also downloads the images of each book
'''

import csv
import os

from bs4 import BeautifulSoup
import requests


def get_content_url(url):
    """Récupérer le contenu d'une page à partir de son url"""
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_list(elements):
    result = []
    for element in elements:
        result.append(element)
    return result


url_category_main = (
    "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
)

content_url_main = get_content_url(url_category_main)

url = url_category_main.replace("index.html", "")

# Get all url's page of the category.
list_page_category = []

check_next_page = content_url_main.find("li", class_="next")

if check_next_page == None:
    list_page_category = [url_category_main]
else:
    next_page = content_url_main.find("li", class_="next").a.get("href")
    clean_next_page = next_page[0:-6]
    url_category_next_page = url + clean_next_page

    page_number = int(content_url_main.find("li", class_="current").text.strip()[-1])

    html = ".html"
    for current_page in range(1, page_number + 1):
        page = f"{url_category_next_page}{current_page}{html}"
        list_page_category.append(page)


# Get all book's url in the category
url_book = []
for url_page in list_page_category:
    content_url = get_content_url(url_page)
    for article in content_url.find_all("article"):
        link = article.find("a")
        url_book.append(
            link.get("href").replace(
                "../../../", "http://books.toscrape.com/catalogue/"
            )
        )


# Récupération des données des bouquins
# Category
category = []
for url in url_book:
    soup = get_content_url(url)
    for categories in soup.find_all("a")[3]:
        category.append(categories)

# Title
title = []
for url in url_book:
    soup = get_content_url(url)
    for titles in soup.find("h1"):
        title.append(titles)

# Rating
all_rating = []
rate = []
rating_dict = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
for url in url_book:
    soup = get_content_url(url)

    for review_rating in soup.find_all("p", class_="star-rating")[0].get("class"):
        rate.append(review_rating)
        rate = [i for i in rate if i != "star-rating"]

for rating in rate:
    all_rating.append(rating_dict[rating] + "/5")

# Product description
product_description = []
for url in url_book:
    soup = get_content_url(url)
    for description in soup.find_all("p")[3]:
        product_description.append(description)

# Upc Price Available
all_upc = []
price_incl_tax = []
price_excl_tax = []
number_available = []

all_td = []
for url in url_book:
    soup = get_content_url(url)
    for upc in soup.find_all("td")[0]:
        all_upc.append(upc)
    for price_incl in soup.find_all("td")[2]:
        price_incl_tax.append(price_incl)
    for price_excl in soup.find_all("td")[3]:
        price_excl_tax.append(price_excl)
    for available in soup.find_all("td")[5]:
        number_available.append(available)

# Url image
all_img_url = []
for url in list_page_category:
    content_url = get_content_url(url)
    for img_url in content_url.find_all("img"):
        all_img_url.append(
            img_url.get("src").replace("../../../../", "https://books.toscrape.com/")
        )


# Write all data in csv file
en_tete = [
    "Category",
    "Title",
    "Rating",
    "UPC",
    "Price_incl_tax",
    "Price_excl_tax",
    "Number_available",
    "Description",
    "Product_page_url",
    "Image_url",
]
with open(f"data_book_of_{category[0]}.csv", "w") as csv_scraper:
    writer = csv.writer(csv_scraper, delimiter=",")
    writer.writerow(en_tete)
    for (
        Category,
        Title,
        Rating,
        UPC,
        Price_incl_tax,
        Price_excl_tax,
        Number_available,
        Description,
        Product_page_url,
        Image_url,
    ) in zip(
        category,
        title,
        all_rating,
        all_upc,
        price_incl_tax,
        price_excl_tax,
        number_available,
        product_description,
        url_book,
        all_img_url,
    ):
        writer.writerow(
            [
                Category,
                Title,
                Rating,
                UPC,
                Price_incl_tax,
                Price_excl_tax,
                Number_available,
                Description,
                Product_page_url,
                Image_url,
            ]
        )

# Download image
directory = os.mkdir(category[0])

url_img_to_download = dict(zip(title, all_img_url))

for title, img in url_img_to_download.items():

    file = open(f"{category[0]}/{title[0:20]}.jpg", "wb")
    response = requests.get(img)
    file.write(response.content)
    file.close()

