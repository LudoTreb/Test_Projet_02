""" Description du script : 
Extraire toutes les données
de tous les livres d'une catégorie
pour les écrire dans un fichier csv
"""

import csv

from bs4 import BeautifulSoup
import requests


def get_url_category():
	"""Récupérer l'url d'une catégorie de livre avec un input()"""
	url = input()
	return url

def get_content_url(url):
	"""Récupérer le contenu d'une page à partir de son url"""
	reponse = requests.get(url)
	page = reponse.content
	soup = BeautifulSoup(page, "html.parser")
	return soup

def get_list(elements):
	result = []
	for element in elements : 
		result.append(element)
	return result

def extract_list_book(url_parse):
	"""Récupérer la liste des url de tous les livres à partir du contenu de l'url catégorie"""

	# Extraire de ce contenu une liste des url des livres
	list_url_book = []
	for article in url_parse.find_all('article'):
		link = article.find("a")
		list_url_book.append(link.get('href').replace('../../../' , 'http://books.toscrape.com/catalogue/')) 
	return list_url_book


def extract_book_data(list_url_book):
	"""Extrait toutes les données du livres à partir de la liste des url des livres et les mettre dans un de dictionnaire"""
	

	title = []
	upc = []

	fieldnames = [
    		"title",
    		"upc",
	]
	data_book = [
    		title,
    		upc,
    		
	]

	for url in list_url_book :
		soup = get_content_url(url)
		titles = soup.find("h1").string
		title = get_list(titles)
		
	print(titles)
	print(type(titles))
	print(len(titles))

	return fieldnames
		

def write_csv(fieldnames):
	"""Créer un fichier csv avec les données des livres"""

	# Écrire dans un fichier csv les données du dictionnaire
	with open("data_book_3.csv", "w") as file_csv:
    		writer = csv.DictWriter(file_csv, delimiter = ";" , fieldnames = fieldnames)
    		writer.writeheader()
    		writer.writerow(
        		{
            		
        		}
    		)




def main():
	"""Point d'entrée principal de mon script"""
	
	category_url = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
	content_url = get_content_url(category_url)

	list_url_book = extract_list_book(content_url)
	print(list_url_book)
	print(type(list_url_book))
	print(len(list_url_book))
	
	# Recupérer sous forme de dictionnaire toutes les infos des livres
	book_data = extract_book_data(list_url_book)
		
	csv_fil = write_csv(book_data)
	
	print("Le fichier csv est crée !")  


if __name__ == "__main__":
	main()