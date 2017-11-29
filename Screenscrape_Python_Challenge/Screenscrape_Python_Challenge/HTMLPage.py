import asyncio, asyncore, argparse, urllib.request, http
from bs4 import BeautifulSoup

class HTMLPage:
    """Creates an HTML object that can be navigated"""

    def getHTMLPage(self, url): # Gets an HTTP(s) page and returns an HTML object
        try:
            self.html = urllib.request.urlopen(url)
            print('we seem to have successfully retrieved {}'.format(url))
            return self.html
        except Exception as e:
            print(e)

    def parsePage(self, HTMLBody):
        self.parsedPage = BeautifulSoup(HTMLBody.read(), 'html.parser')

    def __init__(self, **kwargs):
        self.HTMLBody = self.getHTMLPage(kwargs.get('url'))
        self.parsePage(self.HTMLBody)
        print('searching for \"\'athing\'\"')
        for element in self.parsedPage.find_all('tr'): #search and gather all 'athing' elements in the page. This are the containers for each link.
            try:
                if 'athing' in element.get('class'):
                    print('found it!')
                    print(element.attrs)
                    print(element)
                    print('\n')
                else:
                    pass

            except Exception as e:
                pass

#        print(self.parsedPage.title)
#        print(str(self.parsedPage.contents).encode('utf-8'))