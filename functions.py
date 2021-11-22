import os
import pandas as pd
import requests
from tabulate import tabulate
from datetime import datetime

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def printTickets(table):
    columnList = ["id","created_at","updated_at","subject","status"]
    df = pd.DataFrame(table)
    df["created_at"]=df["created_at"].apply(lambda x: convertFromZulu(x))
    df["updated_at"]=df["updated_at"].apply(lambda x: convertFromZulu(x))
    print(tabulate(df.loc[:,columnList],headers=columnList,showindex=False))

def convertFromZulu(time):
    return str(datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")) + " UTC"

def printIndividualTicket(table,id):
    startID = int(table[0]["id"])
    while(id - startID not in range(0,len(table))):
        print("Valid ID Numbers for this page include "+str(startID)+"-"+str(startID+len(table)-1))
        id = int(input("Inavlid ID entered, please reenter: "))
    clearConsole()
    index = id - startID
    entry = table[index]
    print("Subject: " + entry["subject"])
    print("Status: "+ entry["status"])
    print("ID: "+ str(entry["id"]))
    print('-'*100)
    print("Description:")
    print(entry["description"])
    print('-'*100)
    print("Created at: "+ convertFromZulu(entry["created_at"]))
    print("Updated at: "+ convertFromZulu(entry["updated_at"]))
    print("Submitter ID: " + str(entry["submitter_id"]))
    
def promptUser(prev=False,next=False):
    validInput = ["1","2","q"]
    print("[1] to reprint all entries on the current page")
    print("[2] to view an individual ticket on this page")
    if(prev):
        print("[3] to go to previous page")
        validInput.append("3")
    if(next):
        print("[4] to go to next page")
        validInput.append("4")
    print("[q] to exit")

    command = ""
    while command not in validInput:
        command = input()
        if(command not in validInput):
            print("Invalid Command, please reenter command:")
    return command

def checkCursor(address,username,password):
    if(address is None):
        return False
    r = requests.get(address, auth=(username,password), timeout=2)
    ticketInfo = r.json()
    return bool(ticketInfo["tickets"])