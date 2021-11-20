import requests
import os
import sys
from getpass import getpass

username = input(prompt="Enter your Email Address: ")
password = getpass(prompt="Enter your password: ")


r = requests.get("https://zccjnnanni.zendesk.com/api/v2/tickets.json", auth=(username,password), timeout=2)

ticketInfo = r.json()

if 'error' in ticketInfo.keys():
    print("Error: could not authenticate your username and password")
    print("[1] to retry")
    print("[2] to exit")
    error = input()
    if(error == '1'):
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        exit(1)

