import requests
from bs4 import BeautifulSoup

tmp = requests.get('http://www.google.com')


soup = BeautifulSoup(tmp.content)

#print soup.find_all('a')
print(soup.prettify())


