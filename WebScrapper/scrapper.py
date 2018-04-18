from bs4 import BeautifulSoup
import requests
import dryscrape
import pandas as pd
import numpy as np
import re

def get_armor_links(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x : x and re.compile(url).search(x))
    links = list(map(lambda x : x['href'], a_tags))
    return links

def get_all_armor_links():
    # Armor list urls by body piece
    heads = 'http://kiranico.com/en/mh4u/armor/head'
    chest = 'http://kiranico.com/en/mh4u/armor/chest'
    arms = 'http://kiranico.com/en/mh4u/armor/arms'
    waist = 'http://kiranico.com/en/mh4u/armor/waist'
    legs = 'http://kiranico.com/en/mh4u/armor/legs'

    master_list = []
    urls = [heads, chest, arms, waist, legs]
    for u in urls:
        master_list += get_armor_links(u)
    return master_list

# TODO make a function to interpret slots into integers
# TODO use dryscrape to get data from javascript rendered html
def get_armor_item_data(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    details_general_keys = ['Type', 'Part', 'Gender', 'Rarity', 'Slot', 'Defense']
    details_resist_keys = ['Fire', 'Water', 'Ice', 'Thunder', 'Dragon']
    details_values = []
    
    for key in details_general_keys:
        details_values.append(soup.find('td', string=key).next_sibling.next_sibling.string)

    for key in details_resist_keys:
        details_values.append(soup.find('td', string=key).next_sibling.string)

    details_dict = dict(zip(details_general_keys+details_resist_keys, details_values))

    name = soup.h1.string

    return (name, details_dict)

def build_armor_list_dataframe(url_list):
   pass

#array = get_all_armor_links()
#for w in array:
#    print(w)
#(name, details_dict) = get_armor_item_data(array[0])
#for k in details_dict.items():
#    print(k)

r = requests.get('http://kiranico.com/en/mh4u/armor/legs/leather-trousers')
data = r.text
print(data)
soup = BeautifulSoup(data, 'lxml')

typ = soup.find('td', string='Slot').next_sibling.next_sibling
print(type(typ))