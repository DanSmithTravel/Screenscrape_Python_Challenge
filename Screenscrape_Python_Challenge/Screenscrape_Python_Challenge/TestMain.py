import re, sqlite3, pytest, asyncio, os
import Screenscrape_Python_Challenge
from HTMLPage import HTMLPage
from bs4 import BeautifulSoup
from subprocess import call

def test_commandLineArgs():
    testfilepath = 'output/testOutput.txt'
    if os.path.exists(testfilepath):
        try:
            os.remove(testfilepath)
        except Exception as e:
            raise Exception('Test failing becasue file at {} could not be removed. It may be locked or in use. Error:'.format(testfilepath, e))
    else: pass
    call('py Screenscrape_Python_Challenge.py -s age -p {}'.format(testfilepath)) # run the full app and generate a result file.

    fh = open(testfilepath)
    fileText = fh.read()
    fh.close()
    foundSearchTerm = True if fileText.find('sorted by age') != -1 else False # Look for the sort order keyword in the test file.
    assert foundSearchTerm

def test_stripBadPages():
    testPage = HTMLPage(url = 'https://news.ycombinator.comx/news') # testmode localexec. This page should not exist.
    testPage.DO_NOT_PROCESS = True # mark for deletion
    PageDict = {0:testPage}
    results = [testPage,]
    Screenscrape_Python_Challenge.stripBadPages(PageDict, results) # Bad pages should be stripped out of results.
    assert results == []