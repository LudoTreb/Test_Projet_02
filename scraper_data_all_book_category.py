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
    """
    Retrieve the content of a page from its url
    In parameter we will have a url address as a string
    In return we will have this url parsed. 
    """
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_list(elements):
    """
    Retrieves elements in the form of a list
    In parameter we have one of the element
    which will pass in a loop
    to get all the elements
    and put them in a list 
    """
    result = []
    for element in elements:
        result.append(element)
    return result

def replace_caracter(string,origin,new): 
    """
    Replaces a specific string into a new string 
    Takes as parameter "origin" the characters to replace 
    Takes as parameter "new" the new characters
    In return we have "new_string" the new string 
    """
    new_string = string.replace(origin,new)
    return new_string

url_category_main = (
    "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
)

content_url_main = get_content_url(url_category_main)

url = url_category_main.replace("index.html", "")

# Get all url's page of the category.
list_page_category = []

check_next_page = content_url_main.find("li", class_="next")

if check_next_page == None:
    list_page_category.append(url_category_main)

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

for url in url_book:
    soup = get_content_url(url)
    all_td = soup.find_all("td")
    all_upc.append(all_td[0].text)
    price_incl_tax.append(all_td[2].text)
    price_excl_tax.append(all_td[3].text)
    number_available.append(all_td[5].text)

# Url image
all_img_url = []
for url in list_page_category:
    content_url = get_content_url(url)
    for img_url in content_url.find_all("img"):
        all_img_url.append(
            replace_caracter(img_url.get("src"),"../../../../", "https://books.toscrape.com/")
        )


# Write all data in csv file
columns = [
    "Category",
    "Title",
    "Rating",
    "Upc",
    "Price including tax",
    "Price excluding tax",
    "Number available",
    "Description",
    "Product page url",
    "Image url",
]
data_book = [
    {
        "Category": category,
        "Title": title,
        "Rating": all_rating,
        "Upc": all_upc,
        "Price including tax": price_incl_tax,
        "Price excluding tax": price_excl_tax,
        "Number available": number_available,
        "Description": product_description,
        "Product page url": url_book,
        "Image url": all_img_url,
    }
]
with open(f"data_book_of_{category[0]}.csv", "w", newline="") as file_csv:
    writer = csv.DictWriter(file_csv, delimiter=";", fieldnames=columns)
    writer.writeheader()
    for data in data_book:
        writer.writerow(data)

   
# Reduce the number of characters in the title
reduce_title = []
for titles in title :
    reduce_title.append(titles[0:20])

# Make dictionary with title in key and image in value
url_img_to_download = dict(zip(reduce_title, all_img_url))

# Download image
directory = os.mkdir(category[0])

for titles, img in url_img_to_download.items():

    file = open(f"{category[0]}/{titles}.jpg", "wb")
    response = requests.get(img)
    file.write(response.content)
    file.close()
