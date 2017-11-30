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
    