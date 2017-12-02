# Screenscrape Python Challenge
# Developed by Daniel Smith
# This application will scrape html element data from https://news.ycombinator.com/ and collate that data into a local text file.

import asyncio, asyncore, argparse, urllib.request, http, sqlite3
from concurrent import futures
from HTMLPage import HTMLPage
from TestHTML import test_parsePage, test_bakeLinkDict
from TestHTML import test_createElementDict
from bs4 import BeautifulSoup

def main():


    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(runBlockingTasks())
    loop.close()
    print(results)
       
   #deprecated this in favor of a multithreaded approach.
    #asyncio.gather(process_async_result(pageDict[0].manualInit),
         #              process_async_result(pageDict[1].manualInit),
          #             process_async_result(pageDict[2].manualInit))
           #                 )

    #for page in pageDict:
    #    print('\n\nPrinting contents of {}\n'.format(pageDict.get(page).URL))
    #    for item in pageDict.get(item).bakedDict:
    #        print(item)

async def runBlockingTasks(executor = futures.ThreadPoolExecutor(max_workers = 3)):
    URLlist = {0 : 'https://news.ycombinator.com/news', 1 : 'https://news.ycombinator.com/show', 2 : 'https://news.ycombinator.com/ask'}
    pageDict = dict()
    for item in URLlist:
        pageDict[item] = HTMLPage(url = URLlist.get(item))
    
    loop = asyncio.get_event_loop()
    
    blockingTasks = [
                     loop.run_in_executor(executor, pageDict[0].manualInit),
                     loop.run_in_executor(executor, pageDict[1].manualInit),
                     loop.run_in_executor(executor, pageDict[2].manualInit)
                    ]
    
    completed, pending = await asyncio.wait(blockingTasks)
    results = [t.result() for t in completed]
    return results

async def process_async_result(async_function):
    result = await async_function()
    return result

    #page = HTMLPage(url = 'https://news.ycombinator.com/')
    #page = HTMLPage(testmode = True, testmodeFile = 'testdata\SampleHTML.html', localexec = True)
    #for item in page.bakedDict:
    #    print(page.bakedDict[item])
    #generateTestData.generateParsedPage()
    #x = open('testdata\ElementDictAnswerKey.txt', mode = 'w', encoding = 'utf-8')
    #y = HTMLPage(testmode = True)
    #y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))
    #y.createElementDict(y.parsedPage, y.elementDict)
    #x.write(str(y.elementDict))
    #x.close()

class generateTestData():
    
    def generateBakedLinkDict():
        try:
            dbm = db = sqlite3.connect('testdata/testingHTML.db')
            cursor = db.cursor()
            # create a table for the bakedLinkDict data
            cursor.execute('DROP TABLE IF EXISTS bakedLinkDict')
            cursor.execute('''CREATE TABLE bakedLinkDict(itemID TEXT PRIMARY KEY, id TEXT, headline TEXT,
                            url TEXT, score TEXT, author TEXT, age TEXT, comments TEXT)''')
            db.commit()
        
            # generate data objects 
            y = HTMLPage(testmode = True)
            y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))
            y.createElementDict(y.parsedPage, y.elementDict)
            y.bakeLinkDict(y.elementDict)
            # pull out element data and store it in the table.
            for element in y.bakedDict:
                cursor.execute('''INSERT INTO bakedLinkDict(itemID, id, headline, url, score, author, age, comments)
                                  VALUES(?,?,?,?,?,?,?,?)''', (str(element), str(y.bakedDict[element]['id']),
                                                               str(y.bakedDict[element]['headline']), 
                                                               str(y.bakedDict[element]['URL']),
                                                               str(y.bakedDict[element]['score']),
                                                               str(y.bakedDict[element]['author']),
                                                               str(y.bakedDict[element]['age']),
                                                               str(y.bakedDict[element]['comments']) ))

            db.commit()
        
        except Exception as e:
            print(e)
            db.close()
            dbm.close()
            raise Exception(e)

        db.close()
        dbm.close()
    

if __name__ == '__main__': main()
