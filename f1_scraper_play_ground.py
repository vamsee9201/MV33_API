#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
#%%
url = 'https://www.formula1.com/en/results.html/2023/drivers.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')
#%%
firstNames = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "hide-for-tablet")]
# %%
lastNames = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "hide-for-mobile")]
# %%
driverCodes = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "uppercase hide-for-desktop")]
# %%
driverNationalities = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "dark semi-bold uppercase")]
# %%
driverPoints =  [ span.get_text() for span in soup.find('tbody').find_all(class_ = "dark bold")]
# %%
dataFrameJson = {
    "Code":driverCodes,
    "firstName":firstNames,
    "lastName":lastNames,
    "Nationality":driverNationalities,
    "points":driverPoints
}
# %%
driverTable = pd.DataFrame(dataFrameJson)

# %%
driverTable
# %%
