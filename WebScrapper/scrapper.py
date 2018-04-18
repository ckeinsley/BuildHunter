from bs4 import BeautifulSoup
import requests
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

array = get_all_armor_links()
for w in array:
    print(w)
