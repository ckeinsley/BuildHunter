from bs4 import BeautifulSoup
import requests

url = 'http://kiranico.com/index.php/en/mh3u/weapon/greatsword'
r = requests.get(url)

data = r.text

soup = BeautifulSoup(data, 'lxml')

print(soup.find_all('tr'))