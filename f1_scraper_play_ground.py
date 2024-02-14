#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
#%%
url = 'https://www.formula1.com/en/results.html/2023/races.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')
print(links)
