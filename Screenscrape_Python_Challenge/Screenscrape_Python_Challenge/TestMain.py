import re, sqlite3, pytest, asyncio
import Screenscrape_Python_Challenge
from HTMLPage import HTMLPage
from bs4 import BeautifulSoup
from subprocess import call

def test_commandLineArgs():
    call('py Screenscrape_Python_Challenge.py -s comments')
    fh = open('output/output.txt')
    fileText = fh.read()
    fh.close()
    foundSearchTerm = True if fileText.find('sorted by comments') != -1 else False
    assert foundSearchTerm == True