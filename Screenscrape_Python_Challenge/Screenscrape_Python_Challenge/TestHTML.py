import re, sqlite3, pytest, asyncio
from HTMLPage import HTMLPage
from bs4 import BeautifulSoup


def test_getHTMLPage():
    x = HTMLPage(testmode = True, testmodeFile = 'testdata\SampleHTML.html')
    #run the async getHTMLPage method
    loop = asyncio.new_event_loop() # generate a new loop in case we're already executing in one.
    asyncio.set_event_loop(loop) # set the new loop
             
                # get the HTML page in async testmode
    loop.run_until_complete(
                            asyncio.gather(x.process_async_HTMLBody(x.getHTMLPage, testmode = True, testmodeFile = 'testdata\SampleHTML.html'))
                                )
    loop.close()
                
    assert open('testdata\HTMLSampleAnswerKey.html', encoding = 'utf-8').read() == x.HTMLBody.read()

def test_parsePage():
    answerKey = BeautifulSoup(open('testdata\SampleHTML.html'), "html.parser")
    
    y = HTMLPage(testmode = True)
    loop = asyncio.new_event_loop() # generate a new loop in case we're already executing in one.
    asyncio.set_event_loop(loop) # set the new loop
    loop.run_until_complete(y.parsePage(open('testdata\SampleHTML.html'), testmode = True)) # parse the page async
    loop.close() # loop no longer needed. close it.
    
    #y.parsePage(open('testdata\SampleHTML.html'))

    assert y.parsedPage == answerKey

def test_createElementDict():
    answerKey = dict()  # This block loads the data from the previous SELECT into a dict object

    try:
        dbm = db = sqlite3.connect('testdata/testingHTML.db') # Gotta open the database
        cursor = db.cursor()
        cursor.execute('SELECT * FROM elementDict') # Select the table with reference sample data
        for row in cursor:
            answerKey[row[0]] = row[1]

        db.close()  # gotta close the db, too.
        dbm.close()

    except Exception as e:
        print(e)
        db.close()
        dbm.close()
        raise Exception(e)
    
    # this block below generates live test data and puts it in a dict object.
    # Only the string data is really relevant, and that's all we can test,
    # so the elements are cast into string for this test.

    y = HTMLPage(testmode = True) # make a blank HTMLPage object
    parsedPage = BeautifulSoup(open('testdata\SampleHTML.html'), "html.parser") # parse a page
    y.createElementDict(parsedPage, y.elementDict) # run the live process
    
    testDict = dict() # make a blank dict for use in the assert
    
    for element in y.elementDict: # populate the blank test dict with string elements from the HTMLPage element dict
        testDict[element] = str(y.elementDict[element])
    
    assert testDict == answerKey

def test_bakeLinkDict():
    answerKey = dict() # create a blank dict for our answers
    colNames = ('itemID', 'id', 'headline', 'rank', 'URL', 'score', 'author', 'age', 'comments') # the expected columns columns in the result, so get these from the database for our test data

    try:
        dbm = db = sqlite3.connect('testdata/testingHTML.db') # Gotta open the database
        cursor = db.cursor()
        cursor.execute('SELECT * FROM bakedLinkDict') # Select the table with reference sample data
    except Exception as e:
        print(e)
        db.close()
        dbm.close()
        raise Exception(e)
        
    for row in cursor: # Populate answerKey
        temp = dict() #temporary dict for each iteration of the loop
        try:
            for index, col in enumerate(colNames):
                if index > 0: temp[col] = None if row[index] == 'None' else row[index] #skip the first column since it's the ID in the database.
                                                                                       #Then populate the temp dict with column names and values.
                                                                                       #Set the value to None if it's the 'None' string in the database.
            answerKey[row[0]] = temp # add the completed dict object for the row to the answer key and set its ID to the first value in the row returned by the DB.

        except Exception as e:
            print(e)
            db.close()
            dbm.close()
            raise Exception(e)

    
    db.close()
    dbm.close()



    y = HTMLPage(testmode = True) # generate a blank test object
    parsedPage = BeautifulSoup(open('testdata\SampleHTML.html'), "html.parser") # parse a page
    y.createElementDict(parsedPage, y.elementDict) # Create an element dict on the live object using the ParsedPage sample data.
                                                    # (There's not a good way to avoid using the object's method to do this since the dictionary needs to be populated with HTML objects, not strings from the database.)
    y.bakeLinkDict(y.elementDict) # Bake the dictionary to compare

    assert y.bakedDict == answerKey
