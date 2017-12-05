import re, sqlite3, pytest, asyncio
import Screenscrape_Python_Challenge
from HTMLPage import HTMLPage
from bs4 import BeautifulSoup
from subprocess import call

def test_commandLineArgs():
    call('py Screenscrape_Python_Challenge.py -s age')
    fh = open('output/output.txt')
    fileText = fh.read()
    fh.close()
    foundSearchTerm = True if fileText.find('sorted by age') != -1 else False
    assert foundSearchTerm == True

def test_stripBadPages():
    testPage = HTMLPage(url = 'https://news.ycombinator.comx/news') # testmode localexec. This page should not exist.
    testPage.DO_NOT_PROCESS = True # mark for deletion
    PageDict = {0:testPage}
    results = [testPage,]
    Screenscrape_Python_Challenge.stripBadPages(PageDict, results) # Bad pages should be stripped out of results.
    assert results == []