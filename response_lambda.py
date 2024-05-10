#%%
import boto3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import time
#%%
def handler(event,context):

    #replace year and route values with the ones that are passed through event. 
    print(event)
    request_body = json.loads(event['body'])
    year = request_body["year"]
    route = event["resource"][1:]
    """
    route = "teams"
    year = 2023
    """

    if route == "drivers":
        url = 'https://www.formula1.com/en/results.html/{}/drivers.html'.format(year)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        firstNames = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "hide-for-tablet")]
        lastNames = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "hide-for-mobile")]
        driverCodes = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "uppercase hide-for-desktop")]
        driverNationalities = [ span.get_text() for span in soup.find('tbody').find_all(class_ = "dark semi-bold uppercase")]
        driverPoints =  [ span.get_text() for span in soup.find('tbody').find_all(class_ = "dark bold")]
        driversJson = {
            "Code":driverCodes,
            "firstName":firstNames,
            "lastName":lastNames,
            "Nationality":driverNationalities,
            "points":driverPoints
        }
        returnPayload = {
         "statusCode": 200,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(driversJson)
        }
        return returnPayload

    if route == "teams":
        url = "https://www.formula1.com/en/results.html/{}/team.html".format(year)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        teamNames = [a.get_text() for a in soup.find_all("a",class_ = "dark bold uppercase ArchiveLink")]
        teamPoints = [td.get_text() for td in soup.find_all("td",class_="dark bold")]
        teamJson = {
            "constructorName":teamNames,
            "points":teamPoints
        }
        returnPayload = {
         "statusCode": 200,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(teamJson)
        }
        return returnPayload
    
    if route == "schedule":
        returnPayload = getSchedule(year)
        return returnPayload
    
    if route == "raceidlinks":
        returnPayload = getRaceIdLinks(year)
        return returnPayload

    defaultJSON = {
        "message":"no data"
    }
    return {
        "statusCode": 404,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(defaultJSON)
    }

# %%
"""
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
"""
#%%
def getSchedule(year):
    url = "https://www.formula1.com/en/results.html/{}/races.html".format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print("getting elements >>>")
    elements = soup.find('select',{"class":"resultsarchive-filter-form-select","name":"meetingKey"})
    elements = elements.find_all('option')
    elements = elements[1:]
    print("getting links >>>")
    links = [element.get("value") for element in elements]
    print("getting race Names >>>")
    raceNames = [element.text for element in elements]
    circuitInfos = []
    startDates = []
    endDates = []
    print("getting schedules process started >>>")
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
        #time.sleep(0.2)
    print("finished getting schedules >>>")
    #startDates,endDates = convertDates(startDates,endDates)
    scheduleJson = {
        "raceName":raceNames,
        "circuitInfo":circuitInfos,
        "startDate":startDates,
        "endDate":endDates
    }
    print("returning the payload >>>")
    returnPayload = {
         "statusCode": 200,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(scheduleJson)
        }
    return returnPayload
#%%
def getRaceIdLinks(year):
    url = "https://www.formula1.com/en/results.html/{}/races.html".format(year)
    print("getting respose >>>")
    response = requests.get(url)
    print("converting to soup >>>")
    soup = BeautifulSoup(response.content, 'html.parser')
    optionsList = soup.find('select',{"class":"resultsarchive-filter-form-select","name":"meetingKey"}).find_all("option")
    optionsList
    linksList = []
    for option in optionsList:
        if option.get_text() != "All" :
            link = option.get('value')
            linksList.append(link)
    IdlinksJson = {
        "Idlinks":linksList
    }
    returnPayload = {
         "statusCode": 200,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(IdlinksJson)
        }
    return returnPayload
#%%
def getScheduleFromRaceLink(raceLink,year):
    url = "https://www.formula1.com/en/results.html/{}/races/{}/race-result.html".format(raceLink,year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pElement = soup.find('p', {'class':'date'})
    startDate = pElement.find("span",{'class':'start-date'}).get_text()
    endDate = pElement.find("span",{'class':'full-date'}).get_text()
    circuitInfo = pElement.find("span",{'class':'circuit-info'}).get_text()
    scheduleData = {
        "startDate":startDate,
        "endDate":endDate,
        "circuitInfo":circuitInfo
    }
    returnPayload = {
         "statusCode": 200,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(scheduleData)
        }
    return returnPayload

def getRaceResultFromRaceLink(raceLink,year):
    url = "https://www.formula1.com/en/results.html/{}/races/{}/race-result.html".format(year,raceLink)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find(class_="resultsarchive-table")
    temp = table.find("tbody")
    firstNames = [span.get_text() for span in temp.find_all("span",{"class":"hide-for-tablet"})]
    lastNames = [span.get_text() for span in temp.find_all("span",{"class":"hide-for-mobile"})]
    driverCodes = [span.get_text() for span in temp.find_all("span",{"class":"uppercase hide-for-desktop"})]
    returnDataFrame = pd.DataFrame()
    dfJson = {}

    return None


#%%

"""
if __name__ == "__main__":
    json_data = {
         "body" :
    '{ "year": 2023}',
    "resource":"/raceidlinks"
    }
    response = handler(json_data,context = "hello")
    print(response)
"""


# %%
