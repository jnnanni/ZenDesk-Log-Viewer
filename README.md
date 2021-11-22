Installation:
1. Make sure that you have installed Python 3 on your machine
2. In a terminal at the directory of the program, run the following command:
pip install -r requirements.txt
This will ensure all the proper python packages are installed in order for you
to use the ticket viewer

Usage:
Start the program by using "python3 main.py" in the working directory of the program
The program will ask for your username and password for my zendesk domain
(Done so that I would not have to commit my Username and password to GitHub)
The program will then fetch the first 25 entries from the API and prompt you to input one of the following:
    [1] Reprint the entries on the current page
    [2] View more details on a specific log entry that is part of the current page
    [3] (If a previous page exists) navigate to the previous page of tickets
    [4] (If a next page exists) navigate to the next page of tickets
    [q] Exit the program