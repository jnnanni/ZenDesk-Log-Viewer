import unittest
from functions import *

#Use "python3 funcTests.py < testIn.txt" to run these tests as intended

class TestFunctions(unittest.TestCase):

    def test_convertFromZulu(self):
        self.assertEqual(convertFromZulu("2021-11-20T20:05:02Z"), '2021-11-20 20:05:02 UTC')

    def test_checkCursor(self):
        #Check for moving cursor backwards from first list
        #Cannot have my username and password because of public repo
        #Test passed using my personal info
        username = input()
        password = input()
        self.assertEqual(checkCursor("https://zccjnnanni.zendesk.com/api/v2/tickets.json?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25",username,password),False)
        self.assertEqual(checkCursor("https://zccjnnanni.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25",username,password),True)

    def test_promptUser(self):
        self.assertEqual(promptUser(),"1")
        self.assertEqual(promptUser(),"2")
        #Testing command error checking
        self.assertEqual(promptUser(prev=False),"2")
        self.assertEqual(promptUser(),"q")

    #This code is admittedly tough to unit test in alot of places
    #I used primarily integration testing with the main.py script

if __name__ == '__main__':
    unittest.main()