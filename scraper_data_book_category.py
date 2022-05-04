""" Description du script : 
Extraire toutes les données
de tous les livres d'une catégorie
pour les écrire dans un fichier csv
"""

import csv

from bs4 import BeautifulSoup
import requests


def get_content_url(url):
    """Récupérer le contenu d'une page à partir de son url Parse"""
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_list(elements):
    result = []
    for element in elements:
        result.append(element)
    return result


url_category = (
    "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
)

# Contenu de l'url catégorie
content_url = get_content_url(url_category)

# Recupération de la liste des url des livres de la catégorie
url_book = []
for article in content_url.find_all("article"):
    link = article.find("a")
    url_book.append(
        link.get("href").replace("../../../", "http://books.toscrape.com/catalogue/")
    )


# Récupération des données des bouquins
title = []
for url in url_book:
    soup = get_content_url(url)
    for titles in soup.find("h1"):
        title.append(titles)

category = []
for url in url_book:
    soup = get_content_url(url)
    for categories in soup.find_all("a")[3]:
        category.append(categories)

product_description = []
for url in url_book:
    soup = get_content_url(url)
    for description in soup.find_all("p")[3]:
        product_description.append(description)

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


all_img_url = []
for img_url in content_url.find_all("img"):
    all_img_url.append(img_url.get("src").replace("../../../../" , "https://books.toscrape.com/"))

#print(all_img_url)
#print(type(all_img_url))
#print(len(all_img_url))

# Write all data in csv file
en_tete = [
    "Product_page_url",
    "Category",
    "Title",
    "Description",
    "UPC",
    "Price_incl_tax",
    "Price_excl_tax",
    "Number_available",
    "Rating",
    "Image_url",
]
with open("data_book_One_category.csv", "w") as csv_scraper:
    writer = csv.writer(csv_scraper, delimiter=",")
    writer.writerow(en_tete)
    for (
        Product_page_url,
        Category,
        Title,
        Description,
        UPC,
        Price_incl_tax,
        Price_excl_tax,
        Number_available,
        Rating,
        Image_url
    ) in zip(
        url_book,
        category,
        title,
        product_description,
        all_upc,
        price_incl_tax,
        price_excl_tax,
        number_available,
        all_rating,
        all_img_url,
    ):
        writer.writerow(
            [
                Product_page_url,
                Category,
                Title,
                Description,
                UPC,
                Price_incl_tax,
                Price_excl_tax,
                Number_available,
                Rating,
                Image_url,
            ]
        )