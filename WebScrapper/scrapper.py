from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import pickle
import bson
import re
import sys

# pickle likes to yell if this isn't high
sys.setrecursionlimit(100000000)

# TODO: Store item drops with monsters, just list id's and rates and such
# TODO: Separate out the loading functions from the scraping/writing functions
'''
Generic_Blademaster:
    {
        'id' : '',
        'Name' : '',
        'Weapon_Family' : '',
        'Rarity' : '',
        'Attack' : '',
        'True_Attack' : '',
        'Defense' : '',
        'Affinity' : '',
        'Slot' : '',
        'Price' : '',
        'Element' : {
            'Name' : '',
            'Value' : ''
        }
        'Upgrades_To' : [
            {
                'id' : '',
                'Name' : ''
            }
        ],
        'Upgrade_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'From_Scratch_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ]
    }

Insect_Glaive:
    {
        'id' : '',
        'Name' : '',
        'Weapon_Family' : '',
        'Rarity' : '',
        'Attack' : '',
        'True_Attack' : '',
        'Defense' : '',
        'Affinity' : '',
        'Slot' : '',
        'Price' : '',
        'Element' : {
            'Name' : '',
            'Value' : ''
        }
        'Upgrades_To' : [
            {
                'id' : '',
                'Name' : ''
            }
        ],
        'Upgrade_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'From_Scratch_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'Type' : ''
    }

Charge_Blade_or_Switch_Axe:
    {
        'id' : '',
        'Name' : '',
        'Weapon_Family' : '',
        'Rarity' : '',
        'Attack' : '',
        'True_Attack' : '',
        'Defense' : '',
        'Affinity' : '',
        'Slot' : '',
        'Price' : '',
        'Element' : {
            'Name' : '',
            'Value' : ''
        }
        'Upgrades_To' : [
            {
                'id' : '',
                'Name' : ''
            }
        ],
        'Upgrade_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'From_Scratch_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'Phial' : ''
    }

Bowgun :
    {
        'id' : '',
        'Name' : '',
        'Weapon_Family' : '',
        'Rarity' : '',
        'Attack' : '',
        'True_Attack' : '',
        'Defense' : '',
        'Affinity' : '',
        'Slot' : '',
        'Price' : '',
        'Element' : {
            'Name' : '',
            'Value' : ''
        }
        'Upgrades_To' : [
            {
                'id' : '',
                'Name' : ''
            }
        ],
        'Upgrade_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'From_Scratch_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'Ammo' : [
            {
                'id' : '',
                'Name' : '',
                'Carry' : '',
                'isZoom' : ''
            }
        ]
    }

Bow :
    {
        'id' : '',
        'Name' : '',
        'Weapon_Family' : '',
        'Rarity' : '',
        'Attack' : '',
        'True_Attack' : '',
        'Defense' : '',
        'Affinity' : '',
        'Slot' : '',
        'Price' : '',
        'Element' : {
            'Name' : '',
            'Value' : ''
        }
        'Upgrades_To' : [
            {
                'id' : '',
                'Name' : ''
            }
        ],
        'Upgrade_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'From_Scratch_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'Arc_Shot' : '',
        'Charge_Lvls' : ['', '', '', '']
        'Coatings' : [
            {
                'id' : '',
                'Name' : ''
            }
        ]
    }

Gunlance :
    {
        'id' : '',
        'Name' : '',
        'Weapon_Family' : '',
        'Rarity' : '',
        'Attack' : '',
        'True_Attack' : '',
        'Defense' : '',
        'Affinity' : '',
        'Slot' : '',
        'Price' : '',
         'Element' : {
            'Name' : '',
            'Value' : ''
        }
        'Upgrades_To' : [
            {
                'id' : '',
                'Name' : ''
            }
        ],
        'Upgrade_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'From_Scratch_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ],
        'Shelling' : [
            {'id' : '', 'Name' : ''}
        ]
    }

Armor_Item:
    {
        'id' : '1248329814',
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
            {
                'id' : '1234125',
                'Name' : 'Gathering',
                'Value' : '1'
            },
            {
                'id' : '12314850',
                'Name' : 'Whim',
                'Value' : '3'
            }
        ],
        'Crafting Items' : [
            {
                'id' : '11235143',
                'Name' : 'Warm Pelt' 
                'Quantity': '1'
            },
            {
                'id' : '12341542323',
                'Name' : 'Iron Ore',
                'Quanity' : '1'
            }
        ]
    }

Decoration :
    {
        'id' : '19323214',
        'Name' : 'Leader Jewel 1',
        'Rarity' : '',
        'Carry' : '',
        'Buy' : '',
        'Sell' : '',
        'Craft_Price' : '',
        'Slot' : '',
        'Skills' : [
            {
                'id' : '',
                'Name' : '',
                'Value' : ''
            }
        ],
        'Crafting_Items' : [
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            },
            {
                'id' : '',
                'Name' : '',
                'Quantity' : ''
            }
        ]
    }

Item :
    {
        'id' : '19323214',
        'Name' : 'Potion',
        'Description' : '',
        'Rarity' : '',
        'Carry' : '',
        'Buy' : '',
        'Sell' : '',
        'Combo_List' : [
            {
                'id_1' : '',
                'Name_1' : '',
                'id_2' : '',
                'Name_2' : ''
            },
        ],
        'Gather_Locations' : [
            {
                'Rank' : '',
                'Map' : '',
                'Area' : '',
                'Gather_Method' : '',
                'Quantity' : '',
                'Drop_Rate' : ''
            }
        ]
    }

Monster :
    {
        'id' : '',
        'Name' : '',
        'Item_Drops' : {
            'Low_Rank' : [
                {
                    'Item_Id' : '',
                    'Drop_Type' : '',
                    'Quantity' : '',
                    'Drop_Rate' : ''
                }
            ],
            'High_Rank' : [

            ],
            'G' : [
                
            ]
        },
        'Damage_Chart' : [
            {
                'Region' : '',
                'Cut' : '',
                'Impact' : '',
                'Shot' : '',
                'Fire' : '',
                'Water' : '',
                'Ice' : '',
                'Thunder' : '',
                'Dragon' : '',
                'Dizzy' : ''
            }
        ]
    }

Skill :
    {
        'id' : '',
        'Name' : '',
        'Skills' : [
            {
                'Name' : '',
                'Skill_Req' : 10,
                'Description' : ''
            }
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
WEAPONS = 'http://kiranico.com/en/mh4u/weapon'
MONSTERS = 'http://kiranico.com/en/mh4u/monster'
SKILLS = 'http://kiranico.com/en/mh4u/armor/skill'
ARMORS_PATH = './obj/armors/'
WEAPONS_PATH = './obj/weapons/'
MONSTERS_PATH = './obj/monsters/'
DECORATIONS_PATH = './obj/decorations/'
SKILLS_PATH = './obj/skills/'
ITEMS_PATH = './obj/items/'

def get_all_skill_links():
    r = requests.get(SKILLS)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x : x and re.compile(SKILLS).search(x))
    links = list(map(lambda x : x['href'], a_tags))
    links.pop(0)
    return links

def get_all_monster_links():
    r = requests.get(MONSTERS)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x : x and re.compile(MONSTERS).search(x))
    links = list(map(lambda x : x['href'], a_tags))
    links.pop(0)
    return links

def get_all_item_links():
    r = requests.get(ITEMS)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x : x and re.compile(ITEMS).search(x))
    links = list(map(lambda x : x['href'], a_tags))
    del links[0:4]
    return links

def get_weapon_links(url, driver):
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.findAll('a', href=lambda x : x and re.compile(url).search(x))
    category = a_tags.pop(0).string
    links = list(map(lambda x : x['href'], a_tags))
    return (category,links)

def get_all_weapon_links():
    r = requests.get(WEAPONS)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    a_tags = soup.find_all(href=lambda x: x and re.compile(WEAPONS).search(x))
    weapon_tree_links = list(map(lambda x : x['href'], a_tags))
    weapon_tree_links = weapon_tree_links[:14]
    weapon_categories = []
    link_arrays = []

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./env/chromedriver')
    driver.set_page_load_timeout(WEBDRIVER_REQUEST_TIMEOUT)
    

    for link in weapon_tree_links:
        attempts = 0
        while True:
            try:
                (category, links) = get_weapon_links(link, driver)
                link_arrays.append(links)
                weapon_categories.append(category)
            except TimeoutException:
                print('TimeoutException: Attempt ', attempts)
                attempts += 1
                continue
            break
    return dict(zip(weapon_categories, link_arrays))

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
    urls = [HEAD, CHEST, ARMS, WAIST, LEGS]
    for u in urls:
        master_list += get_armor_links(u)
    return master_list

def get_name_from_url(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    name = soup.find('h1').string
    if name == None:
        name = soup.find('h1').contents[0].strip()
    return name

def write_name_id_mapping():
    master_id = 0
    item_links = get_all_item_links()
    armor_links = get_all_armor_links()
    weapon_temp = get_all_weapon_links()
    weapon_links = []
    for w in weapon_temp.values():
        weapon_links += w
    monster_links = get_all_monster_links()
    skill_links = get_all_skill_links()

    name_id_map = {}
    link_array = [item_links, armor_links, weapon_links, monster_links, skill_links]
    link_prefixes = ['ITEM', 'ARMOR', 'WEAPON', 'MONSTER', 'SKILL']

    for k in range(len(link_array)):
        for url in link_array[k]:
            print(url)
            name = get_name_from_url(url)
            name = link_prefixes[k] + ':' + name
            if name_id_map.get(name) != None:
                print('AAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHH!!!!!!!!')
                print('Name: ', name)
            name_id_map[name] = master_id
            master_id += 1
    print('Next Available Id')
    f = open('./obj/name_id_map.p', 'wb')
    pickle.dump(name_id_map, f)
    f.close()

def read_name_id_mapping():
    f = open('./obj/name_id_map.p', 'rb')
    name_id_mapping = pickle.load(f, encoding='unicode')
    f.close()
    return name_id_mapping

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

def process_armor_item_data(url, driver, name_id_map):
   
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
    uid = name_id_map.get('ARMOR:' + name)
    price = soup.find('h3', string='Crafting Materials').next_sibling.next_sibling.contents[1].contents[0].contents[1].string
    price = re.sub('Price: ', '', price)
    skills = get_armor_item_skills(soup, name_id_map)
    crafting_items = get_armor_crafting_items(soup, name_id_map)

    armor_item_dict['id'] = uid
    armor_item_dict['Name'] = name
    armor_item_dict['Price'] = price
    armor_item_dict['Skills'] = skills
    armor_item_dict['Crafting Items'] = crafting_items

    return armor_item_dict

def get_armor_item_skills(bsoup, nam_id_map):
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
        uid = nam_id_map.get('SKILL:' + name)
        value = tds[3].string.replace('+', '')
        skills.append(
            {
                'id':uid,
                'Name':name,
                'Value':value
            }
        )
        k += 2
    return skills

def get_armor_crafting_items(bsoup, name_id_map):
    trs = bsoup.find('h3', string='Crafting Materials').next_sibling.next_sibling.contents[1].contents
    crafting_items = []
    k = 2
    while k < len(trs):
        name = trs[k].td.a.string
        uid = name_id_map.get('ITEM:' + name)
        quantity = trs[k].td.next_sibling.next_sibling.string
        crafting_items.append(
            {
                'id' : uid,
                'Name': name,
                'Quantity': quantity
            })
        k += 2
    return crafting_items
        
def populate_armor_items_list():
    name_id_map = read_name_id_mapping()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./env/chromedriver')
    driver.set_page_load_timeout(WEBDRIVER_REQUEST_TIMEOUT)
    url_list = get_all_armor_links()
    armor_list = []
    id_list = []
    for url in url_list:
        attempts = 0
        while True:
            try:
                temp = process_armor_item_data(url, driver, name_id_map)
            except TimeoutException:
                print('TimeoutException: ', attempts)
                attempts += 1
                continue
            break
        print(temp)
        armor_list.append(temp)
        id_list.append(temp['id'].replace(' ','')) # TODO replace with id attributes
    return (armor_list, id_list)

def write_armor_files():
    (armor_item_list, id_list) = populate_armor_items_list()
    id_file = open(ARMORS_PATH + 'id_list.p', 'wb')
    pickle.dump(id_list, id_file)
    id_file.close()
    for item in armor_item_list:
        # TODO: replace name with id for filenames
        item_file = open(ARMORS_PATH + str(item['id']).replace(' ', '') + '.p', 'wb')
        pickle.dump(item, item_file)
        item_file.close()

def is_jewel(soup):
    header = soup.find('h1').string
    return bool(header) and bool(re.compile('(Jewel)|(Jwl)').search(header))

def get_combo_list(soup, name_id_map):
    combo_header = soup.find('h2', string=lambda x : x and re.compile('Where to find.*').search(x)).next_sibling.next_sibling.next_sibling.next_sibling
    combo_header = combo_header.find('h3', string='Combo List')
    if combo_header == None:
        return []
    combo_list = []
    table_rows = combo_header.next_sibling.next_sibling.contents[1].contents[0].find_next_siblings('tr')
    for row in table_rows:
        links = row.find_all('a')
        if len(links) != 3:
            print('ComboListError')
            for l in links:
                print(l)
            return
        name_1 = links[1].string
        name_2 = links[2].string
        uid_1 = name_id_map.get('ITEM:' + name_1)
        uid_2 = name_id_map.get('ITEM:' + name_2)
        combo_list.append({
            'id_1' : uid_1,
            'Name_1' : name_1,
            'id_2' : uid_2,
            'Name_2' : name_2
        })
    return combo_list

def get_gather_locations(soup):
    no_results = soup.find('h3', string='Maps').find_next_sibling('p')
    gather_locations = []
    if no_results == None:
        rows = soup.find('h3', string='Maps').find_next_sibling('table').find_all('tr')
        for r in rows:
            datas = r.find_all('td')
            gather_locations.append({
                'Rank' : datas[0].string,
                'Map' : datas[1].a.string,
                'Area' : datas[2].string,
                'Gather_Method' : datas[3].string,
                'Quantity' : datas[4].string,
                'Drop_Rate' : datas[5].string
            })
    return gather_locations    

def process_item_data(url, driver, name_id_map):
    # need to determine whether an item is a 'crafting/consumable/misc' item, a 'decoration', or 'monster shit'
    print(url)
    driver.get(url)
    time.sleep(0.3)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    if is_jewel(soup):
        print('Its a jewel')
        return None
    else:
        name = soup.find('h1').string
        uid = name_id_map.get('ITEM:' + name)
        description = soup.find('h1').next_sibling.next_sibling.string
        rarity = soup.find('td', string='Rarity').next_sibling.next_sibling.string
        carry = soup.find('td', string='Carry').next_sibling.next_sibling.string
        buy = soup.find('td', string='Buy').next_sibling.next_sibling.string
        sell = soup.find('td', string='Sell').next_sibling.next_sibling.string
        combo_list = get_combo_list(soup, name_id_map)
        gather_locations = get_gather_locations(soup)
        return {
            'id' : uid,
            'Name' : name,
            'Description' : description,
            'Rarity' : rarity,
            'Carry' : carry,
            'Buy' : buy,
            'Sell' : sell,
            'Combo_List' : combo_list,
            'Gather_Locations' : gather_locations
        }
        
def populate_items_list():
    name_id_map = read_name_id_mapping()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./env/chromedriver')
    driver.set_page_load_timeout(WEBDRIVER_REQUEST_TIMEOUT)
    links = get_all_item_links()

    id_list = []
    for k in links:
        attempts = 0
        while True:
            try:
                temp = process_item_data(k, driver, name_id_map)
            except TimeoutException:
                print('TimeoutException: ', attempts)
                attempts += 1
                if attempts % 10 == 0:
                    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./env/chromedriver')
                continue
            break
        if temp == None:
            continue
        print(temp)
        print('Begin writing', temp['Name'])
        item_file = open(ITEMS_PATH + str(temp['id']) + '.bson', 'wb')
        item_file.write(bson.dumps(temp))
        item_file.close()
        print('Finished writing,', temp['Name'])
        id_list.append(temp['id'])
    print('Populated complete')
    print('Beginning write')
    id_dict = {'ids' : id_list}
    id_file = open(ITEMS_PATH + 'id_dict.bson', 'wb')
    id_file.write(bson.dumps(id_dict))
    id_file.close()
    print('ID file wirtten')
    

def write_item_files():
    (item_list, id_list) = populate_items_list()
    print('Populated complete')
    print('Beginning write')
    id_file = open(ITEMS_PATH + 'id_list.p', 'wb')
    pickle.dump(id_list, id_file)
    id_file.close()
    print('ID file wirtten')
    for item in item_list:
        print('Begin writing', item['Name'])
        item_file = open(ITEMS_PATH + str(item['id']) + '.p', 'wb')
        pickle.dump(item, item_file)
        item_file.close()
        print('Finished writing,', item['Name'])
    print('End writing')


def process_skill_data(url, driver, name_id_map):
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    
    name = soup.find('h1').string
    uid = name_id_map.get('SKILL:' + name)
    description = soup.find('h1').next_sibling.next_sibling.p.string
    skills = []

    skill_table = soup.find('tbody').contents
    k = 0
    while k < len(skill_table):
        skill_name = skill_table[k].contents[1].string
        skill_req = skill_table[k].contents[3].string
        skill_description = skill_table[k].contents[5].string
        skills.append({
            'Name' : skill_name,
            'Skill_Req' : skill_req.strip().replace('+',''),
            'Description' : skill_description
        })
        k += 2
    return {
        'id' : uid,
        'Name' : name,
        'Description' : description,
        'Skills' : skills
    }

def populate_skills_list():
    name_id_map = read_name_id_mapping()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./env/chromedriver')
    driver.set_page_load_timeout(WEBDRIVER_REQUEST_TIMEOUT)
    url_list = get_all_skill_links()
    skill_list = []
    id_list = []
    for url in url_list:
        attempts = 0
        while True:
            try:
                temp = process_skill_data(url, driver, name_id_map)
            except TimeoutException:
                print('TimeoutException: ', attempts)
                attempts += 1
                continue
            break
        print(temp)
        if temp == None:
            continue
        skill_list.append(temp)
        id_list.append(temp['id'])
    return (skill_list, id_list)

def write_skills_file():
    (skill_list, id_list) = populate_skills_list()
    id_file = open(SKILLS_PATH + 'id_list.p', 'wb')
    pickle.dump(id_list, id_file)
    id_file.close()
    for skill in skill_list:
        skill_file = open(SKILLS_PATH + str(skill['id']) + '.p', 'wb')
        pickle.dump(skill, skill_file)
        skill_file.close()

populate_items_list()