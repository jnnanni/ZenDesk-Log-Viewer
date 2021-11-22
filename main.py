import requests
import os
import sys
from getpass import getpass
import json
import pandas as pd
from tabulate import tabulate
from datetime import datetime

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def printPage(link,username,password):
    clearConsole()
    print("Fetching ticket data...")
    r = requests.get(link, auth=(username,password), timeout=2)
    clearConsole()
    ticketInfo = r.json()
    #printTableInfo(ticketInfo["tickets"])
    printIndividualTicket(ticketInfo["tickets"],35)

def printTableInfo(table):
    columnList = ["id","type","created_at","updated_at","subject","status"]
    df = pd.DataFrame(table)
    print(tabulate(df.loc[:,columnList],headers=columnList,showindex=False))

def convertFromZulu(time):
    return str(datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")) + " UTC"

def printIndividualTicket(table,id):
    startID = table[0]["id"]
    print(startID)
    entry = table[id - startID]
    print("Subject: " + entry["subject"])
    print("Status: "+ entry["status"])
    print('-'*100)
    print("Description:")
    print(entry["description"])
    print('-'*100)
    print("Created at: "+ convertFromZulu(entry["created_at"]))
    print("Updated at: "+ convertFromZulu(entry["updated_at"]))
    print("Submitter ID: " + str(entry["submitter_id"]))


username = input("Enter your Email Address: ")
#password = getpass(prompt="Enter your password: ")
password = input("Enter your password: ")

clearConsole()

print("Fetching ticket data...")
r = requests.get("https://zccjnnanni.zendesk.com/api/v2/tickets.json", auth=(username,password), timeout=2)
clearConsole()

ticketInfo = r.json()

if 'error' in ticketInfo.keys():
    print("ERROR: could not authenticate your username and/or password")
    print(" [1] to retry")
    print(" Any other key to exit")
    error = input()
    if(error == '1'):
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        exit(1)


print("Successfully fetched Ticket Data")
page = 0

file = open('test.json', 'w')
json.dump(ticketInfo,file,indent=6)
file.close()

