#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
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
"""
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
"""
#%%
startDatesSample = ['29 Feb',
  '07',
  '22',
  '05',
  '19',
  '03',
  '17',
  '24',
  '07',
  '21',
  '28',
  '05',
  '19',
  '26',
  '23',
  '30 Aug',
  '13',
  '20',
  '18',
  '25',
  '01',
  '21',
  '29 Nov',
  '06']
endDatesSample = ['02 Mar 2024',
  '09 Mar 2024',
  '24 Mar 2024',
  '07 Apr 2024',
  '21 Apr 2024',
  '05 May 2024',
  '19 May 2024',
  '26 May 2024',
  '09 Jun 2024',
  '23 Jun 2024',
  '30 Jun 2024',
  '07 Jul 2024',
  '21 Jul 2024',
  '28 Jul 2024',
  '25 Aug 2024',
  '01 Sep 2024',
  '15 Sep 2024',
  '22 Sep 2024',
  '20 Oct 2024',
  '27 Oct 2024',
  '03 Nov 2024',
  '23 Nov 2024',
  '01 Dec 2024',
  '08 Dec 2024']

#%%
def convertDates(startDates,endDates):
    startDatesUpdated  = []
    for index,date in enumerate(startDates):
        if len(date) == 2:
            date = date + " " + endDates[index][3:]
        else :
            date = date + " " +endDates[index][7:]
        startDatesUpdated.append(date)
    #converting to datetime
    format = "%d %b %Y"
    parsedStartDates = []
    parsedEndDates = []
    for date in startDatesUpdated:
        parsedStartDate = datetime.strptime(date, format)
        parsedStartDates.append(parsedStartDate)
    for date in endDates:
        parsedEndDate = datetime.strptime(date, format)
        parsedEndDates.append(parsedEndDate)

    return (parsedStartDates,parsedEndDates)
# %%
def getSchedule(year):
    url = "https://www.formula1.com/en/results.html/{}/races.html".format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find('select',{"class":"resultsarchive-filter-form-select","name":"meetingKey"})
    elements = elements.find_all('option')
    elements = elements[1:]
    links = [element.get("value") for element in elements]
    raceNames = [element.text for element in elements]
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
    startDates,endDates = convertDates(startDates,endDates)
    scheduleJson = {
        "raceName":raceNames,
        "circuitInfo":circuitInfos,
        "startDate":startDates,
        "endDate":endDates
    }
    return scheduleJson
#%%
getSchedule(2024)
# %%
