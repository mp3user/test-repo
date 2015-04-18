import os 
import sys
import re 
import requests 
from bs4 import BeautifulSoup

ebay_page_url = raw_input("Your url: ")
def build_list_of_links(ebay_page_url):
    page = requests.get(page_url).text
    soup = BeautifulSoup(page)
    list_of_links = []
    for item in soup.find_all('a', {'itemprop':'name'}):
        list_of_links.append(item.get('href'))
    return(list_of_links)

def write_links_file(output_links_file, links_list):
    with open(file_destination, "a") as output_file:
        link_writer = csv.writer(output_file)
        link_writer.writerow(links_list)