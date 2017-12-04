# Screenscrape Python Challenge
# Developed by Daniel Smith
# This application will scrape html element data from https://news.ycombinator.com/ and collate that data into a local text file.

import asyncio, asyncore, argparse, urllib.request, http, sqlite3
from operator import *
from concurrent import futures
from HTMLPage import HTMLPage
from TestHTML import test_parsePage, test_bakeLinkDict
from TestHTML import test_createElementDict
from bs4 import BeautifulSoup

def main():
    
#    HTMLPage(testmode = True, testmodeFile = 'testdata\SampleHTML.html', localexec = True) # testmode localexec
    
    #get command line arguments and define the sort order to be used.
    validArgs = ('rank', 'id', 'score', 'age', 'comments')
    cmdArgs = getCmdArgs(validArgs)
    if any(x in cmdArgs.sortOrder for x in validArgs): pass
    else: cmdArgs.sortOrder = 'score'
    #print(cmdArgs.sortOrder) # diagnostic message

    URLlist = {0 : 'https://news.ycombinator.com/news', 1 : 'https://news.ycombinator.com/show', 2 : 'https://news.ycombinator.com/ask'}
    pageDict = dict()

    #initialize our objects
    for index in URLlist:
        pageDict[index] = HTMLPage(url = URLlist.get(index))

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(runBlockingTasks(pageDict)) # execute object actions asynchronously
    loop.close()

    writeResultsToFile(results, 'output\output.txt', sortOrder = cmdArgs.sortOrder)
   
def getCmdArgs(validArgs):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action = 'store', dest = 'sortOrder', help = 'Specify the sort order. Defaults to \'score\' Acceptable values are: {}'.format(validArgs))
    return parser.parse_args()
    

def writeResultsToFile(results, filepath = 'output\output.txt', sortOrder = 'score'):
    '''Write HTML page results to the passed in file. Overwrites previous data.'''
    
    fh = open(filepath, mode = 'w')
    print('\nOpened {} for writing results.\n'.format(filepath)) # Diagnostic message
    
    for page in results: # Iterate through each page
        print('Writing results sorted by {} from {} to file: {}.'.format(sortOrder, page.URL, filepath)) #Diagnostic message
        try:
            fh.write('###NEW SECTION###\n\n\nWriting sorted data for {}\nThe data is sorted by {}\n\n'.format(page.URL, sortOrder)) # Write the section header with the page URL
            for s in sorted(page.bakedDict.items(), key=lambda x:int(0 if getitem(x[1],sortOrder) == None else getitem(x[1],sortOrder))): # Use the Sorted function to help iterate through the Page's baked dictionary. Sorts using the passed in header.
                #print(s[1]['headline']) #Diagnostic message
                for linkData in s[1]: #Iterate through each link group in the baked dict.
                    if linkData != 'URL' and linkData != 'id':  #Don't write the URL or the uniqueID to file.
                        fh.write('{}: {}\n'.format(linkData, s[1].get(linkData))) # Write the key/value pair from the baked dictionary.
                fh.write('\n') #spacer for readability.
        except Exception as e:
            print('Encountered an error. Moving on to the next page, if available. Error:')
            print(e)
            #fh.close()

    print('\nFinished writing to file. Seems we didn\'t encounter any errors!\n')
    fh.close() #close the file when we're all done writing.


async def runBlockingTasks(tasks, executor = futures.ThreadPoolExecutor()):
    """Executes object initialization asynchronously and builds a dictionary of completed objects to return."""
        
    loop = asyncio.get_event_loop() # Get the event loop
    
    blockingTasks = [ # run each task in a new thread
                     loop.run_in_executor(executor, tasks[i].manualInit) for i in tasks
                    ]
    
    completed, pending = await asyncio.wait(blockingTasks) # Wait for all tasks to complete. Put them in "completed"
    results = [t.result() for t in completed] # Pull the result object from the returned future. Add it to the results dictionary.
    return results


class generateTestData():
    '''Execute methods in this class to generate test data from a sample HTML file.'''
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
            loop = asyncio.new_event_loop() # generate a new loop in case we're already executing in one.
            asyncio.set_event_loop(loop) # set the new loop
            loop.run_until_complete(y.parsePage(open('testdata\SampleHTML.html'), testmode = True)) # parse the page async
            loop.close() # loop no longer needed. close it.
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
