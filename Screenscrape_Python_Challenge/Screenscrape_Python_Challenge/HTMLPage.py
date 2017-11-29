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

    def createElementDict(self, parsedPage, dictionary):
        print('trying...')
        for element in parsedPage.find_all('tr'): #search and gather all 'athing' elements in the page. This are the containers for each link.
            #print('trying to iterate...')
            try:
                if 'athing' in element.get('class'):
             #       print('found it!')
             #       print(element.get('id'))
             #       print(element.attrs)
             #       print(element)
             #       print('\n')
                    id = element.attrs['id']
             #       print('we we\'ll try to assign ID {} as the dict item.'.format(id))
                    dictionary[id] = element
                    dictionary['{}-data'.format(id)] = element.next_sibling
                    #print('looks like the dictionary element got set to:\n{}'.format(dictionary.get(id)))
                    #temp = self.linkDict['id']
                    
                else:
                    pass

            except Exception as e:
                pass 

    def getHeadline(self, element):
        #print(element.attrs['class'])
        for tag in element.find_all('a'):
            #print(tag)
            #print(tag.attrs)
            #print('storylink' in tag.get('class'))

            try:
                if 'storylink' in tag.get('class'):
                    #print('found a link')
                    #print(tag.get('href'))
                    return tag.next_element
                else:
                    pass
            except:
                pass
    
    def getURL(self, element):
        for tag in element.find_all('a'):
            try:
                if 'storylink' in tag.get('class'):
                    #print('found a link')
                    return tag.get('href')
                else:
                    pass
            except:
                pass

    def getPoints(self, element):
        print(element)
        for tag in element.find_all('span'):
            try:
                if 'score' in tag.get('class'):
                    return tag.next_element
                else:
                    pass
            except:
                pass

    def __init__(self, **kwargs):
        #declare variables
        self.linkDict = dict()
         
        self.HTMLBody = self.getHTMLPage(kwargs.get('url'))
        self.parsePage(self.HTMLBody)
        #print('searching for \"\'athing\'\"')
        self.createElementDict(self.parsedPage, self.linkDict)
        
        #print(self.linkDict.get('15786855')) # prints a test that existed in the dict on 29 Nov.
        print(self.getHeadline(self.linkDict.get('15786855')))
        print(self.getURL(self.linkDict.get('15786855')))
        print('Score of this link is {}'.format(self.getPoints(self.linkDict.get('15786855-data'))))

#        print(self.parsedPage.title)
#        print(str(self.parsedPage.contents).encode('utf-8'))