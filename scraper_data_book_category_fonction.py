"""
Script Description:
Extract all data of all books in all category
to write them to a csv file.
Also downloads the images of each book
"""

import csv
import os

from bs4 import BeautifulSoup
import requests


def get_content_url(url):
    """
    Récupére le contenu d'une page à partir de son url
    En paramètre on aura une adresse url sous forme d'une chaine de caractère
    En retour on aura cette url parsée.
    """
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup

def replace_caracter(string,origin,new): 
    """
    Replaces a specific string into a new string 
    Takes as parameter "origin" the characters to replace 
    Takes as parameter "new" the new characters
    In return we have "new_string" the new string 
    """
    new_string = string.replace(origin,new)
    return new_string


def convert_rating(rate):
    """
    Convertir des nombres qui sont en chaine de caractere
    en alpha numérique 
    En parametre on recoit un nombre en chaine de caractere
    Qui passe dans un dictionnaire qui renvoit ce nombre en alpha numérique
    et on le présente sous forme de note sur 5 
    exemple "Four" --> "4" --> "4/5"
    En retour on a la note sur 5
    """
    rating_dict = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    rating = rating_dict[rate] + "/5"
    return rating



def extract_book_details(url: str):
    """
    Recupère tous les éléments dur la page d'un livre
    En paramètre on a une une string url
    La fonction va chercher tous les éléments
    et les rangent dans un dictionnaire
    En retour on a ce dictionnaire
    """
    soup = get_content_url(url)
    category = soup.find_all("a")[3].string
    title = soup.find("h1").string
    description = []#soup.find_all("p")[3].string
    rating = convert_rating(soup.find_all("p", class_="star-rating")[0].get("class")[1])
    upc = soup.find_all("td")[0].string
    price_incl_tax = soup.find_all("td")[2].string
    price_excl_tax = soup.find_all("td")[3].string
    number_available = soup.find_all("td")[5].string
    img_url = replace_caracter(soup.find("img").get("src"),"../../","https://books.toscrape.com/" )
    product_url = url
    
    book = {
        "category": category,
        "title": title,
        "description": description,
        "rating": rating,
        "upc": upc,
        "price_incl_tax": price_incl_tax,
        "price_excl_tax": price_excl_tax,
        "number_available": number_available,
        "img_url": img_url,
        "product_url": product_url,
    }

    return book

def extract_book_url(url:str):
    """
    Récupère toutes les url des livres d'une catégorie
    En paramètres on a une string url 
    La fonction va chercher toutes les url des livres 
    pour une catégorie et les rangent dans une liste.
    En retour on a cette liste
    """
    list_url_book =[]
    soup = get_content_url(url)
    for article in soup.find_all("article"):
        link = article.find("a")
        list_url_book.append(replace_caracter(link.get("href"),"../../../", "http://books.toscrape.com/catalogue/"))

    return list_url_book

def extract_category_page_url(url):
    """
    Récupère toutes les url des pages d'une catégorie 
    En paramètres on a une string url 
    La fonction vérifie si il y a plusieurs page/url à la catégorie
    Si non on retourne une liste avec seulement l'url de la page
    Si oui on retourne une liste avec l'url de toutes les pages de la catégorie.
    En retour on a donc cette liste
    """
    soup = get_content_url(url)
    
    url_clean  = replace_caracter(url,"index.html", "")
    
    check_next_page = soup.find("li", class_="next")

    list_page_category = []
    if check_next_page == None:
        list_page_category.append(url)

    else:
        next_page = check_next_page.a.get("href")
        clean_next_page = next_page[0:-6]
        url_category_next_page = url_clean + clean_next_page

        page_number = int(soup.find("li", class_="current").text.strip()[-1])

        html = ".html"
        for current_page in range(1, page_number + 1):
            page = f"{url_category_next_page}{current_page}{html}"
            list_page_category.append(page)

    return list_page_category

def extract_category_url(url):
    """
    Récupère toutes les url des catégories 
    En paramètres on a une string url 
    La fonction va chercher toutes les url des catégories
    Et les range dans une liste
    En retour on a cette liste
    """
    soup = get_content_url(url)

    url_clean  = replace_caracter(url,"index.html", "")

    list_category = []
    for link in soup.find("div", class_="side_categories").find_all("a"):
        list_category.append(url_clean + link.get("href"))

    del list_category[0]

    return list_category


def write_csv():
    """
    Ecrire les infos récupérés dans un fichier csv
    En paramètre on a notre dictionnaire rempli de données ?
    La fonction va écrire dans un fichier csv 
    toutes les données récupérer sur les livre 
    pour une catégorie de livre
    Le nom du fichier csv a le nom de la catégorie.
    """
    columns = [] #l'entete peut-etre recupérer avec le dictionnaire ? juste les clés 
    data_book = [] #ici notre dictionnaire

    with open(f"data_book_of_{category[0]}.csv", "w", newline="") as file_csv:
        writer = csv.DictWriter(file_csv, delimiter=";", fieldnames=columns)
        writer.writeheader()
        writer.writerows(databook)


def download_img():
    """
    Télécharge toutes les images des livres d'une catégorie dans un dossier
    En paramètre on a notre dictionnaire rempli de données ? 
    La fonction créer un dossier au nom de la catégorie
    et écrit dans le dossier toutes les images de des livres de la catégorie.
    """
    # reduce the number of characters in the title
    reduce_title = []
    for titles in title:
        reduce_title.append(titles[0:20])

    # Download image
    directory = os.mkdir(category[0])

    url_img_to_download = dict(zip(reduce_title, all_img_url))

    for titles, img in url_img_to_download.items():

        file = open(f"{category[0]}/{titles}.jpg", "wb")
        response = requests.get(img)
        file.write(response.content)
        file.close()


if __name__ == "__main__":

    url = "https://books.toscrape.com/index.html"
    test = extract_category_url(url) 

print(test)
print(len(test))
print(type(test))
