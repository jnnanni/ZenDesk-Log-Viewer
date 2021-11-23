import sys
from getpass import getpass
from requests.exceptions import TooManyRedirects
from requests.models import HTTPError
from functions import *

f = open("domain.cfg","r")
config = f.readlines()
config = [val.rstrip() for val in config]
address = config[1]+"/api/v2/tickets.json?page[size]=25"
if(config[3] not in ["0","1"]):
    print("Error in domain.cfg: \'Input Redirection for Password\' must be set to either 0 or 1")
    exit(1)
username = input("Enter your Email Address: ")
if(bool(int(config[3]))):
    password = input("Enter your password: ")
else:
    password = getpass(prompt="Enter your password: ")


while(True):
    try:
        clearConsole()
        print("Fetching ticket data...")
        r = requests.get(address, auth=(username,password), timeout=2)
        clearConsole()
        break
    except(TimeoutError,ConnectionError,HTTPError,TooManyRedirects) as e: #Error Checking for initial read
            print("Error Encountered in Initial API Request:")
            print(e)
            print("[1] to retry")
            print("[q] to exit")
            command = input()
            while(command not in ["1","q"]):
                print("[1] to retry")
                print("[q] to exit")
                command = input()
            if(command == "1"):
                continue
            if(command == "q"):
                exit(1)

ticketInfo = r.json()
if "error" in ticketInfo.keys(): #Error Checking for Username/Password and Subdomain
    if(type(ticketInfo["error"])==type({})):
        if("No help desk at" in ticketInfo["error"]["title"]):
            print("ERROR: Invalid Domain found in domain.cfg, please check the file before retrying")
    else:
        print("ERROR: could not authenticate your username and/or password")
    print("[1] to retry")
    print("[q] to exit")
    command = input()
    while(command not in ["1","q"]):
        print("[1] to retry")
        print("[q] to exit")
        command = input()
    if(command == "1"):
        os.execv(sys.executable, ["python"] + sys.argv)
    elif(command == "q"):
        exit(1)

print("Successfully fetched Ticket Data")

page = 1
command = ""
firstPageView = True
while(command!="q"):
    try:
        prev = checkCursor(ticketInfo["links"]["prev"],username,password)
        next = checkCursor(ticketInfo["links"]["next"],username,password)
        if firstPageView:
            clearConsole()
            printTickets(ticketInfo["tickets"])
            firstPageView = False
        print("Current Page: " + str(page))
        command = promptUser(prev,next)
        if(command == "1"):
            clearConsole()
            printTickets(ticketInfo["tickets"])
            continue
        if(command == "2"):
            clearConsole()
            printTickets(ticketInfo["tickets"])
            command = int(input("Choose an ID to view: "))
            printIndividualTicket(ticketInfo["tickets"],command)
            continue
        if(command == "3"):
            clearConsole()
            firstPageView = True
            r = requests.get(ticketInfo["links"]["prev"], auth=(username,password), timeout=2)
            ticketInfo = r.json()
            page = page - 1
            continue
        if(command == "4"):
            clearConsole()
            firstPageView = True
            r = requests.get(ticketInfo["links"]["next"], auth=(username,password), timeout=2)
            ticketInfo = r.json()
            page = page + 1
            continue
    except(TimeoutError,ConnectionError,HTTPError,TooManyRedirects,KeyError) as e: #Error Checking for input loop
        print("Error Encountered in API Request")
        print(e)
        print("[1] to retry")
        print("[q] to exit")
        command = input()
        while(command not in ["1","q"]):
            print("[1] to retry")
            print("[q] to exit")
            command = input()
        if(command == "1"):
            clearConsole()
            continue
        if(command == "q"):
            break

