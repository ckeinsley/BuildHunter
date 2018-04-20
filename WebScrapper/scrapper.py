from bs4 import BeautifulSoup
import requests
import dryscrape
import pandas as pd
import numpy as np
import re
import webkit_server
import time

'''
{
    Name : 'Leather Trousers',
    Type : 'All',
    Part : 'Head',
    Gender : 'Both',
    Rarity : '1',
    Defense : '1 — 71',
    Slot : 'o--',
    Fire : '-1',
    Water : '0',
    Ice : '0',
    Thunder : '0',
    Dragon : '+1',
    Skills : [
        ('Gathering', '+1'),
        ('Whim', '+3')
    ]
}
'''
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
def get_armor_item_data(url, session):
    # r = requests.get(url)
    # data = r.text
    retry_count = 25
    while True:
        try:
            session.visit(url)
        except (webkit_server.InvalidResponseError, webkit_server.EndOfStreamError, BrokenPipeError, ConnectionRefusedError, ConnectionResetError) as e:
            time.sleep(5)
            if retry_count == 0:
                break
            print('URL: ', url)
            print("ERROR: {}".format(e.args[-1]))
            session.reset()
            retry_count -= 1
            continue
        break
    response = session.body()
    soup = BeautifulSoup(response, 'lxml')

    details_general_keys = ['Type', 'Part', 'Gender', 'Rarity', 'Defense']
    special_slot = ['Slot']
    details_resist_keys = ['Fire', 'Water', 'Ice', 'Thunder', 'Dragon']
    details_values = []
    
    for key in details_general_keys:
        details_values.append(soup.find('td', string=key).next_sibling.next_sibling.string)

    # Slot is special
    details_values.append(soup.find('td', string='Slot').next_sibling.next_sibling.contents[0].string)

    for key in details_resist_keys:
        details_values.append(soup.find('td', string=key).next_sibling.string)

    armor_item_dict = dict(zip(details_general_keys + special_slot + details_resist_keys, details_values))

    name = soup.h1.string
    price = soup.find('h3', string='Crafting Materials').next_sibling.next_sibling.contents[1].contents[0].contents[1].string
    price = re.sub('Price: ', '', price)
    skills = get_armor_item_skills(soup)
    crafting_items = get_armor_crafting_items(soup)

    armor_item_dict['Name'] = name
    armor_item_dict['Price'] = price
    armor_item_dict['Skills'] = skills
    armor_item_dict['Crafting Items'] = crafting_items

    return armor_item_dict

def get_armor_item_skills(bsoup):
    table_rows = bsoup.find('h3', string='Skills').next_sibling.next_sibling.contents[1].contents
    skills = []
    k = 0
    while k < len(table_rows):
        tds = table_rows[k].contents
        name = tds[1].a.string
        value = tds[3].string
        skills.append((name, value))
        k += 2
    return skills

def get_armor_crafting_items(bsoup):
    trs = bsoup.find('h3', string='Crafting Materials').next_sibling.next_sibling.contents[1].contents
    crafting_items = []
    k = 2
    while k < len(trs):
        name = trs[k].td.a.string
        quantity = trs[k].td.next_sibling.next_sibling.string
        crafting_items.append((name, quantity))
        k += 2
    return crafting_items
        

def populate_armor_items():
    url_list = get_all_armor_links()
    session = dryscrape.Session()
    armor_list = []
    for url in url_list:
        time.sleep(3)
        armor_list.append(get_armor_item_data(url, session))
    print(armor_list)
    return armor_list

   
populate_armor_items()

#array = get_all_armor_links()
#(name, details_dict) = get_armor_item_data(array[0])
#print(details_dict)
#for k in details_dict.items():
#    print(k)

#session = dryscrape.Session()
#while True:
#    try:
#        session.visit('http://kiranico.com/en/mh4u/armor/head/derring-headgear')
#    except (webkit_server.InvalidResponseError, webkit_server.EndOfStreamError):
#        continue
#    break
#response = session.body()
#soup = BeautifulSoup(response, 'lxml')

#print(get_armor_crafting_items(soup))
#print(get_armor_item_data('http://kiranico.com/en/mh4u/armor/legs/derring-trousers'))

#typ = soup.find('a', string='Gathering').parent.next_sibling.next_sibling.contents[0].string
#print(typ)