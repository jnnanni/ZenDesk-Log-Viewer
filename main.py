import sys
from getpass import getpass
from requests.exceptions import TooManyRedirects
from requests.models import HTTPError
from functions import *

username = input("Enter your Email Address: ")
password = getpass(prompt="Enter your password: ")
#Uncomment 10 and comment 8 for use with input redirection
#password = input("Enter your password: ")
address = "https://zccjnnanni.zendesk.com/api/v2/tickets.json?page[size]=25"

while(True):
    try:
        clearConsole()
        print("Fetching ticket data...")
        r = requests.get(address, auth=(username,password), timeout=2)
        clearConsole()
        break
    except(TimeoutError,ConnectionError,HTTPError,TooManyRedirects): #Error Checking for initial read
            print("Error Encountered in API Request")
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

if "error" in ticketInfo.keys(): #Error Checking for Username/Password
    print("ERROR: could not authenticate your username and/or password")
    print(" [1] to retry")
    print(" Any other key to exit")
    error = input()
    if(error == "1"):
        os.execv(sys.executable, ["python"] + sys.argv)
    else:
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
    except(TimeoutError,ConnectionError,HTTPError,TooManyRedirects,KeyError): #Error Checking for input loop
        print("Error Encountered in API Request")
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

