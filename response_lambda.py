#%%
import boto3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
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

    defaultJSON = {
        "message":"no data"
    }
    return {
        "statusCode": 404,
        'headers': {'Content-Type': 'application/json'},
        "body":json.dumps(defaultJSON)
    }

#%%

"""
if __name__ == "__main__":
    json_data = {
        "year":"2022"
    }
    response = handler(json_data,context = "hello")
    print(response)
"""

# %%