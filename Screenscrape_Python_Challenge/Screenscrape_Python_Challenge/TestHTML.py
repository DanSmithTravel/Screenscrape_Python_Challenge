import re, sqlite3, pytest
from HTMLPage import HTMLPage
from bs4 import BeautifulSoup


def test_getHTMLPage():
    x = HTMLPage(testmode = True)
    assert open('testdata\HTMLSampleAnswerKey.html', encoding = 'utf-8').read() == x.getHTMLPage(testmode = True).read()

def test_parsePage():
    answerKey = BeautifulSoup(open('testdata\ParsedPageAnswerKey.txt','rb'), "html.parser")
    y = HTMLPage(testmode = True)
    y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))#, encoding = 'utf-8'))
    #print(y.parsedPage.encode('utf-8'))
    assert y.parsedPage == answerKey

def test_createElementDict():
    try:
        dbm = db = sqlite3.connect('testdata/testingHTML.db') # Gotta open the database
        cursor = db.cursor()
        cursor.execute('SELECT * FROM elementDict') # Select the table with reference sample data
    except Exception as e:
        print(e)
        db.close()
        dbm.close()
        raise Exception(e)
    
    answerKey = dict()  # This block loads the data from the previous SELECT into a dict object
    for row in cursor:
        answerKey[row[0]] = row[1]

    db.close()  # gotta close the db, too.
    dbm.close()

    # this block generates live test data and puts it in a dict object.
    # Only the string data is really relevant, and that's all we can test,
    # so the elements are cast into string for this test.
    y = HTMLPage(testmode = True)   
    y.parsePage(open('testdata\HTMLSampleAnswerKey.html'))
    y.createElementDict(y.parsedPage, y.elementDict)
    testDict = dict()
    for element in y.elementDict:
        testDict[element] = str(y.elementDict[element])
    
    assert testDict == answerKey

    