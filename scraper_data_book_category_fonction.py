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
    Get the content of web page from is url.

            Parameters:
                    url (str): A string

            Returns:
                    soup (str): the url parsed
    """
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")
    return soup


def replace_caracter(string, origin, new):
    """
    Replaces a specific string into a new string

            Parameters:
                    string (str): the string with caracter to replace
                    origin (str): the character to replace
                    new (str): the new characters

            Returns:
                    new_tring (str): the new string with caractere replaced
    """
    new_string = string.replace(origin, new)
    return new_string


def convert_rating(rate):
    """
    Convert number that are string to alpha numeric

            Parameters:
                    rate (string): numbre in string

            Returns:
                    rating (string): number in alpha numeric and on five
                                        example: "Four"-->"4"-->"4/5"

    """
    rating_dict = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    rating = rating_dict[rate] + "/5"
    return rating


def extract_book_details(url: str):
    """
    Get all details on ulr of a book

            Parameters:
                    url (str): a url of one book

            Returns:
                    book (dict): a dictionary with all details of a book
    """
    soup = get_content_url(url)
    category = soup.find_all("a")[3].string
    title = soup.find("h1").string
    description = soup.find_all("p")[3].string
    rating = convert_rating(soup.find_all("p", class_="star-rating")[0].get("class")[1])
    upc = soup.find_all("td")[0].string
    price_incl_tax = soup.find_all("td")[2].string
    price_excl_tax = soup.find_all("td")[3].string
    number_available = soup.find_all("td")[5].string
    img_url = replace_caracter(
        soup.find("img").get("src"), "../../", "https://books.toscrape.com/"
    )
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


def extract_book_url(url: str):
    """
    Get all url's book of one category

            Parameters:
                    url (str): a url's page of category

            Returns:
                    list_url_book (list): a list of url's book
    """
    list_url_book = []
    soup = get_content_url(url)
    for article in soup.find_all("article"):
        link = article.find("a")
        list_url_book.append(
            replace_caracter(
                link.get("href"), "../../../", "http://books.toscrape.com/catalogue/"
            )
        )

    return list_url_book


def extract_category_page_url(url):
    """
    Get all url's page of one category

            Parameters:
                    url (str): a url category

            Returns:
                    list_page_category (list): a list of url's page of one category
    """
    soup = get_content_url(url)

    url_clean = replace_caracter(url, "index.html", "")

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
    Get all url's category

            Parameters:
                    url (str): url of the website

            Returns:
                    list_category (list): a list of url's category
    """
    soup = get_content_url(url)

    url_clean = replace_caracter(url, "index.html", "")

    list_category = []
    for link in soup.find("div", class_="side_categories").find_all("a"):
        list_category.append(url_clean + link.get("href"))

    del list_category[0]

    return list_category


def write_csv(dictionary):
    """
    Write a csv file for each category from a dictionary

            Parameters:
                    dictionary (dict): dictionary of all the book's details of one category

            Returns:
                    .csv: a csv file for each category

    """
    columns = [
        "category",
        "title",
        "description",
        "rating",
        "upc",
        "price_incl_tax",
        "price_excl_tax",
        "number_available",
        "img_url",
        "product_url",
    ]

    data_book = dictionary

    with open(
        f"exports/{data_book[0]['category']}/data_book_of_{data_book[0]['category']}.csv", "w", newline=""
    ) as file_csv:
        writer = csv.DictWriter(file_csv, delimiter=";", fieldnames=columns)
        writer.writeheader()
        writer.writerows(data_book)


def download_img(dictionary):
    """
    Download all book's image for each category in a specific directory.

            Parameters:
                    dictionary (dict): dictionary of all the book's details of one category

            Returns:
                    .jpg: all image's book for each category in specific directory

    """
    # reduce the number of characters in the title and clean it
    reduce_clean_title = []
    for titles in dictionary:
        list_title = titles.get("title")
        reduce_clean_title.append(replace_caracter(list_title[0:20], "/", "_"))

    list_img_url = []
    for url in dictionary:
        all_url_img = url.get("img_url")
        list_img_url.append(all_url_img)

    # Download image
    directory = os.makedirs(f"exports/{dictionary[0]['category']}/images")

    url_img_to_download = dict(zip(reduce_clean_title, list_img_url))

    for titles, img in url_img_to_download.items():

        file = open(f"exports/{dictionary[0]['category']}/images/{titles}.jpg", "wb")
        response = requests.get(img)
        file.write(response.content)
        file.close()


def main():

    """
    Main function get all details of book for all categories
    Write them in csv file and dowload images of the books
    """

    # get a list of categories from the main url of the site.
    list_category = extract_category_url("https://books.toscrape.com/index.html")
    counter = []
    # get a list of all url's pages for each category
    for url in list_category:
        counter.append(url)
        list_page_category = extract_category_page_url(url)

        # get a list of all book's details
        list_book_details = []
       
        for page_url in list_page_category:
            list_book_url = extract_book_url(page_url)

            for book in list_book_url:

                details = extract_book_details(book)
                list_book_details.append(details)
        

        print(f"{len(counter)}/50 The {list_book_details[0]['category']} category being extracted")

        download_img(list_book_details)

        write_csv(list_book_details)


if __name__ == "__main__":
    main()
