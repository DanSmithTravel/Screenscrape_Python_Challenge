# Screenscrape Python Challenge
# Developed by Daniel Smith
# This application will scrape html element data from https://news.ycombinator.com/ and collate that data into a local text file.

import asyncio, asyncore, argparse, urllib.request, http, sqlite3, re
from operator import *
from concurrent import futures
from HTMLPage import HTMLPage
from TestHTML import test_parsePage, test_bakeLinkDict
from TestHTML import test_createElementDict
from bs4 import BeautifulSoup

def main():
    
#    HTMLPage(testmode = True, testmodeFile = 'testdata\SampleHTML.html', localexec = True) # testmode localexec

    #get command line arguments and define the sort order to be used.
    validSortArgs = ('rank', 'id', 'score', 'age', 'comments')
    cmdArgs = getCmdArgs(validSortArgs)
    if cmdArgs.sortOrder == None:
        cmdArgs.sortOrder = 'score' # set the default sort order to 'score' if no sort arg was passed
        print('No arguments set. Using default sort order of \'Score\'\n')
    else:
        if any(x in cmdArgs.sortOrder for x in validSortArgs): print('Invalid sort order. Using default sort order of \'Score\'\n')
        else: cmdArgs.sortOrder = 'score' # set the default sort order to 'score' if an invalid arg was passed.
    
    # define the list of URLs to scrape.
    URLlist = {0 : 'https://news.ycombinator.com/news', 1 : 'https://news.ycombinator.com/show', 2 : 'https://news.ycombinator.com/ask'}
    
    # Initialize a dictionary of blank pages.
    pageDict = dict()
    for index in URLlist:
        pageDict[index] = HTMLPage(url = URLlist.get(index))

    #populate all the pages in the page dictionary
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(runBlockingTasks(pageDict)) # execute object actions asynchronously
    loop.close()

    #removes the page from the dictionary if there was an error gathering the page from URL.
    for page in pageDict:
        if pageDict[page].DO_NOT_PROCESS == True:
            del results[results.index(pageDict[page])]
            print('\nPage at {} could not be retrieved, so it\'s been marked for deletion from the page dictionary.'.format(pageDict[page].URL))

    #Write everything to file using the sort order specified by the command line args.
    if cmdArgs.filePath == None:
            writeResultsToFile(results, sortOrder = cmdArgs.sortOrder)
    else:
        writeResultsToFile(results, filepath = cmdArgs.filePath, sortOrder = cmdArgs.sortOrder)
   
def getCmdArgs(validSortArgs):
    '''Pulls commmand line arguments and returns the parsed object.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action = 'store', dest = 'sortOrder', help = 'Specify the sort order. Defaults to \'score\' Acceptable values are: {}'.format(validSortArgs))
    parser.add_argument('-p', action = 'store', dest = 'filePath', help = 'specify the explicit or relative file path to output data to. Defaults to \'output\'output.txt if not set.')
    return parser.parse_args()
    

def writeResultsToFile(results, filepath = 'output\output.txt', sortOrder = 'score'):
    '''Write HTML page results to the passed in file. Overwrites previous data. Create a new file if the existing file is locked.'''
    
    try: # Try to open the passed in file
        fh = open(filepath, mode = 'w+')
        print('\nOpened {} for writing results.\n'.format(filepath)) # Diagnostic message
    except Exception as e:
        newfilepath = '{}.new{}'.format(re.search('.*?.[^.]*', filepath).group(0), re.search('[.].+', filepath).group(0)) # create a new filepath. Insert '.new' before the existing file extension.
        print('Couldn\'t seem to open the file for writing. Maybe it\'s in use?. Trying to create a new file instead at {}'.format(newfilepath)) # Diagnostic message
        filepath = newfilepath
        try:
            fh = open(filepath, mode = 'w+') #try to open the new file in write-create mode.
            
        except Exception as e:
            raise Exception('Could create the new file at {}!\nError: {}'.format(newfilepath), e)
    
    for page in results: # Iterate through each page
        print('Writing results sorted by {} from {} to file: {}.'.format(sortOrder, page.URL, filepath)) #Diagnostic message
        try:
            fh.write('###NEW SECTION###\n\n\nWriting sorted data for {}\nThe data is sorted by {}\n\n'.format(page.URL, sortOrder)) # Write the section header with the page URL
            for s in sorted(page.bakedDict.items(), key=lambda x:(int(0 if getitem(x[1],sortOrder) == None else getitem(x[1],sortOrder)), # Use the Sorted function to help iterate through the Page's baked dictionary. Sorts using the passed in header. 
                                                                  int(0 if getitem(x[1], 'rank') == None else getitem(x[1], 'rank')))): # Use a secondary sort order of rank.
                for linkData in s[1]: #Iterate through each link group in the baked dict.
                    if linkData != 'URL' and linkData != 'id':  #Don't write the URL or the uniqueID to file.
                        fh.write('{}: {}\n'.format(linkData, s[1].get(linkData))) # Write the key/value pair from the baked dictionary.
                fh.write('\n') #spacer for readability.
        
        except Exception as e:
            print('Encountered an error. Moving on to the next page, if available. Error:')
            print(e)

    print('\nFinished writing to file.\n')
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
                            rank TEXT, url TEXT, score TEXT, author TEXT, age TEXT, comments TEXT)''')
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
                cursor.execute('''INSERT INTO bakedLinkDict(itemID, id, headline, rank, url, score, author, age, comments)
                                  VALUES(?,?,?,?,?,?,?,?,?)''', (str(element),
                                                               str(y.bakedDict[element]['id']),
                                                               str(y.bakedDict[element]['headline']), 
                                                               str(y.bakedDict[element]['rank']),
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
