from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
import pickle
import re
import webkit_server
import time
import sys

# pickle likes to yell if this isn't high
sys.setrecursionlimit(10000)

# TODO: Add item ids, constantly increasing, keep track of max, make skills and crafting items 
# TODO: Will need to add id's to skills and crafting items so I can put those with the armors

'''
{
    Name : 'Leather Trousers',
    Type : 'All',
    Part : 'Head',
    Gender : 'Both',
    Rarity : '1',
    Defense : {
        'initial' : '1',
        'max' : '71'
    }
    Slot : '1',
    Fire : '-1',
    Water : '0',
    Ice : '0',
    Thunder : '0',
    Dragon : '1',
    Skills : [
        ('Gathering', '1'),
        ('Whim', '3')
    ],
    'Crafting Items' : [
        ('Warm Pelt', '1'),
        ('Iron Ore', '1')
    ]
}
'''

# CONSTANTS:
WEBDRIVER_REQUEST_TIMEOUT = 5
HEAD = 'http://kiranico.com/en/mh4u/armor/head'
CHEST = 'http://kiranico.com/en/mh4u/armor/chest'
ARMS = 'http://kiranico.com/en/mh4u/armor/arms'
WAIST = 'http://kiranico.com/en/mh4u/armor/waist'
LEGS = 'http://kiranico.com/en/mh4u/armor/legs'
ITEMS = 'http://kiranico.com/en/mh4u/item'
ARMOR_ITEMS_PATH = './obj/armor_items/'



def get_armor_links(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x : x and re.compile(url).search(x))
    links = list(map(lambda x : x['href'], a_tags))
    return links

def get_all_armor_links():
    # Armor list urls by body piece
    master_list = []
    #urls = [head, chest, arms, waist, legs] DON'T FORGET TO REVERT THIS
    urls = [HEAD]
    for u in urls:
        master_list += get_armor_links(u)
    return master_list

# TODO make a function to interpret slots into integers

def slot_encoder(slot_string):
    switcher = {
        '---' : 0,
        'o--' : 1,
        'oo-' : 2,
        'ooo' : 3
    }
    return switcher.get(slot_string)

def defense_range_encoder(range_string):
    vals = re.findall(r'[\d]+', range_string)
    if len(vals) != 2:
        print('You done fucked up!!!!!')
        return {
            'initial' : 'ERROR',
            'max' : 'ERROR'
        }
    else:
        return {
            'initial' : vals[0],
            'max' : vals[1]
        }

def process_armor_item_data(url, driver):
   
    driver.get(url)
    # time.sleep(0.25)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')

    details_general_keys = ['Type', 'Part', 'Gender', 'Rarity']
    special_slot = ['Slot', 'Defense']
    details_resist_keys = ['Fire', 'Water', 'Ice', 'Thunder', 'Dragon']
    details_values = []
    
    for key in details_general_keys:
        details_values.append(soup.find('td', string=key).next_sibling.next_sibling.string)

    # Slot is special
    details_values.append(slot_encoder(soup.find('td', string='Slot').next_sibling.next_sibling.contents[0].string))
    details_values.append(defense_range_encoder(soup.find('td', string='Defense').next_sibling.next_sibling.string))

    for key in details_resist_keys:
        details_values.append(soup.find('td', string=key).next_sibling.string.replace('+', ''))

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
    table_rows = bsoup.find('h3', string='Skills').next_sibling.next_sibling.contents
    skills = []
    if len(table_rows) >= 2:
        table_rows = table_rows[1].contents
    else :
        return skills
    k = 0
    while k < len(table_rows):
        tds = table_rows[k].contents
        name = tds[1].a.string
        value = tds[3].string.replace('+', '')
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
        
def populate_armor_items_list():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./env/chromedriver')
    driver.set_page_load_timeout(WEBDRIVER_REQUEST_TIMEOUT)
    url_list = get_all_armor_links()
    armor_list = []
    id_list = []
    count = 0 # TODO: Get rid of
    for url in url_list:
        attempts = 0
        while True:
            try:
                temp = process_armor_item_data(url, driver)
            except TimeoutException:
                print('TimeoutException: ', attempts)
                attempts += 1
                continue
            break
        print(temp)
        armor_list.append(temp)
        id_list.append(temp['Name'].replace(' ','')) # TODO replace with id attributes
        count += 1 # TODO: Get rid of
        if count == 10: # TODO: Get rid of
            break # TODO: Get rid of
    return (armor_list, id_list)

def write_armor_files():
    (armor_item_list, id_list) = populate_armor_items_list()
    id_file = open(ARMOR_ITEMS_PATH + 'id_list.p', 'wb')
    pickle.dump(id_list, id_file)
    id_file.close()
    for item in armor_item_list:
        # TODO: replace name with id for filenames
        item_file = open(ARMOR_ITEMS_PATH + item['Name'].replace(' ', '') + '.p', 'wb')
        pickle.dump(item, item_file)
        item_file.close()

def read_armor_files():
    id_file = open(ARMOR_ITEMS_PATH + 'id_list.p', 'rb')
    id_list = pickle.load(id_file)
    id_file.close()
    armor_item_list = []
    for item in id_list:
        item_file = open(ARMOR_ITEMS_PATH + item + '.p', 'rb')
        armor_item_list.append(pickle.load(item_file))
        item_file.close()
    for i in armor_item_list:
        print(i)
    return (armor_item_list, id_list)

def get_all_item_links():
    r = requests.get(ITEMS)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x : x and re.compile(ITEMS).search(x))
    links = list(map(lambda x : x['href'], a_tags))
    return links

def process_item_data(url, driver):
    # need to determine whether an item is a 'crafting/consumable/misc' item, a 'decoration', or 'monster shit'
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')

    


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