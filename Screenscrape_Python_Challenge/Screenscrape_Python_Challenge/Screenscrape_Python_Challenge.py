# Screenscrape Python Challenge
# Developed by Daniel Smith
# This application will scrape html element data from https://news.ycombinator.com/ and collate that data into a local text file.

import asyncio, asyncore, argparse, urllib.request, http, sqlite3
from HTMLPage import HTMLPage
from TestHTML import test_parsePage
from TestHTML import test_createElementDict
from bs4 import BeautifulSoup

def main():
        #page = HTMLPage(url = 'https://news.ycombinator.com/')
        #page = HTMLPage(testmode = True,)
        #test_parsePage()
        
        """  
        dbm = db = sqlite3.connect('testdata/testingHTML.db')
        cursor = db.cursor()
        cursor.execute('CREATE TABLE elementDict(id TEXT PRIMARY KEY, payload TEXT)')
        db.commit()
        try:

            y = HTMLPage(testmode = True)
            y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))
            y.createElementDict(y.parsedPage, y.elementDict)
            for element in y.elementDict:
                cursor.execute('''INSERT INTO elementDict(id, payload)
                                  VALUES(?,?)''', (str(element), str(y.elementDict.get(element))))
                
            db.commit()
        except Exception as e:
            print(e)
            db.close()
            dbm.close()

        """
        #x = open('testdata\ElementDictAnswerKey.txt', mode = 'w', encoding = 'utf-8')
        #y = HTMLPage(testmode = True)
        #y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))
        #y.createElementDict(y.parsedPage, y.elementDict)
        #x.write(str(y.elementDict))
        #x.close()
        test_createElementDict()
        #for link in page.bakedDict:
        #    print(page.bakedDict.get(link))
                
    

if __name__ == '__main__': main()
