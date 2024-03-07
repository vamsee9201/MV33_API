#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
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

#getting the team table. 
#%%
url = "https://www.formula1.com/en/results.html/2023/team.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
#%%
teamNames = [a.get_text() for a in soup.find_all("a",class_ = "dark bold uppercase ArchiveLink")]
# %%
teamPoints = [td.get_text() for td in soup.find_all("td",class_="dark bold")]
teamPoints
# %%
teamJson = {
    "constructorName":teamNames,
    "points":teamPoints
}
# %%
teamTable = pd.DataFrame(teamJson)
teamTable

# %%
url = "https://www.formula1.com/en/results.html/2024/races.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# %%
allRaces = soup.find('select',{"class":"resultsarchive-filter-form-select","name":"meetingKey"})
# %%
allRaces = allRaces.find_all('option')
allRaces = allRaces[1:]
#%%
links = [element.get("value") for element in allRaces]
# %%
raceNames = [element.text for element in allRaces]
# %%
raceNames
#%%
examplelink = "1229/bahrain"
url = "https://www.formula1.com/en/results.html/2024/races/{}/race-result.html".format(examplelink)
url
#%%
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# %%
info = soup.find('span',{"class":"circuit-info"}).text
start_date = soup.find('span',{"class":"start-date"}).text
end_date = soup.find('span',{"class":"full-date"}).text
#%%

def getSchedule(year):
    url = "https://www.formula1.com/en/results.html/{}/races.html".format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find('select',{"class":"resultsarchive-filter-form-select","name":"meetingKey"})
    elements = elements.find_all('option')
    elements = elements[1:]
    links = [element.get("value") for element in elements]
    circuitInfos = []
    startDates = []
    endDates = []
    for link in links:
        url = "https://www.formula1.com/en/results.html/{}/races/{}/race-result.html".format(year,link)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        circuitInfo = soup.find('span',{"class":"circuit-info"}).text
        circuitInfos.append(circuitInfo)
        startDate = soup.find('span',{"class":"start-date"}).text
        startDates.append(startDate)
        endDate = soup.find('span',{"class":"full-date"}).text
        endDates.append(endDate)
        time.sleep(1)
    scheduleJson = {
        "startDate":startDates,
        "endDate":endDates,
        "circuitInfo":circuitInfos
    }
    return scheduleJson
#%%
getSchedule(2024)



# %%
