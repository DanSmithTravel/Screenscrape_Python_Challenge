# Screenscrape Python Challenge
# Developed by Daniel Smith
# This application will scrape html element data from https://news.ycombinator.com/ and collate that data into a local text file.

import asyncio, asyncore, argparse, urllib.request, http
from HTMLPage import HTMLPage
from TestHTML import test_parsePage
from bs4 import BeautifulSoup

def main():
        #page = HTMLPage(url = 'https://news.ycombinator.com/')
        #page = HTMLPage(testmode = True,)
        #test_parsePage()
        x = open('testdata\ParsedPageAnswerKey.txt', mode = 'wb')
        y = HTMLPage(testmode = True)
        y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))
        x.write(y.parsedPage.encode_contents())
        x.close()
        #for link in page.bakedDict:
        #    print(page.bakedDict.get(link))
                
    

if __name__ == '__main__': main()
