import io, asyncio, asyncore, argparse, urllib.request, http, re, unicodedata
from bs4 import BeautifulSoup

class HTMLPage:
    """Creates an HTML object that can be navigated"""

    def getHTMLPage(self, url = "", testmode = False): # Gets an HTTP(s) page and returns an HTML object
        if testmode:
            try:
                return open('SampleHTML.html', encoding = 'utf-8')

            except Exception as e:
                print(e)

        else:
            try:
                return urllib.request.urlopen(url)
            
            except Exception as e:
                print(e)

    def parsePage(self, HTMLBody):  #parses the HTML body into a BeautifulSoup object.
        try:
            self.parsedPage = BeautifulSoup(HTMLBody.read(), 'html.parser')
        except Exception as e:
            print('There was an error trying to parse the page. Error:\n{}'.format(e)) #Diagnostic message


    def createElementDict(self, parsedPage, dictionary): # create a dictionary of all link groups
        #print('trying...')
        for element in parsedPage.find_all('tr'): #search and gather all 'athing' elements in the page. This are the containers for each link.
            #print('trying to iterate...')
            try:
                if 'athing' in element.get('class'): # a link group in the HTML has the class 'athing' skip all others.
                    element.append(element.next_sibling) #combine main link element group with the next one that contains additional properties like score.
                    id = element.attrs['id']
                    dictionary[id] = element    #set the key/value  pair in the dictionary to [uniqueID : data object]

            except Exception as e:
                #diagnostic
                pass 

    def getHeadline(self, element):     #find the 'storylink' in the given link group element. Extract the headline text.
        #print(element) #Diagnostic message
        for tag in element.find_all('a'):
            try:
                if 'storylink' in tag.get('class'):
                    #print('found a link') #Diagnostic message
                    return self.replaceUnicodeChars(tag.next_element)

            except Exception as e:
                #print(e)    
                pass
    
    def getURL(self, element):      #Search through all <a> tags in the link group element. Extract the URL that corresponds to the headline text.
        for tag in element.find_all('a'):
            try:
                if 'storylink' in tag.get('class'):
                    #print('found a link')  #diagnostic message
                    return tag.get('href')

            except:
                pass

    def getPoints(self, element):   #Search through all <span> tags in the link group element for the 'score' class. Extract the number of points.
        for tag in element.find_all('span'):
            try:
                if 'score' in tag.get('class'):
                    return tag.next_element

            except:
                pass
    
    def getAuthor(self, element):   #Search through all <a> tags in the link group element and find the 'hnuser' class. Extract the submitters username.
        # this method can return None if the story was submitted anonymously.
        for tag in element.find_all('a'):
            try:
                if 'hnuser' in tag.get('class'):
                    return tag.next_element
            except:
                pass

    def getAge(self, element, trim=False): #returns age of post in 'xx minutes/hours/days ago'. If trim=True, method returns a flat digit value.
        for tag in element.find_all('span'):
            try:
                if 'age' in tag.get('class'):
                    if trim: return re.search('\\d+', tag.next_element.next_element).group(0) #returns just the first group of digits in the string, i.e. the number of hours/minutes
                    else: return tag.next_element.next_element

            except:
                pass

    def getNumComments(self, element, trim=False):  #Search through all <a href> tags in the link group element and find the one that includes the word 'comments' in the link display text. If trim=True, method returns a flat digit value.
        # this method can return None if no one has commented on the story.
        for tag in element.find_all('a'):
            try:
               if element.attrs['id'] in tag.get('href') and 'comments' in tag.next_element:
                   if trim: return str.replace(tag.next_element,'\xa0comments', "") 
                   else: return str(str.replace(tag.next_element,'\xa0', " ")).encode('utf-8')

            except:
                pass

    def bakeLinkDict(self, uncookedLinkDict):   #Assembles a dictionary of formatted name/value pairs for relevant link information.
        
        for rawLinkGroup in uncookedLinkDict:
                temp = dict()   #Put all the local data into a temporary dictionary to group it.
                
                temp['id'] = rawLinkGroup
                temp['headline'] = self.getHeadline(uncookedLinkDict[rawLinkGroup])
                #temp['URL'] = self.getURL(uncookedLinkDict[rawLinkGroup])  #Makes diag output difficult to read. Re-enable later.
                temp['score'] = self.getPoints(uncookedLinkDict[rawLinkGroup])
                temp['author'] = self.getAuthor(uncookedLinkDict[rawLinkGroup])
                temp['age'] = self.getAge(uncookedLinkDict[rawLinkGroup])
                temp['comments'] = self.getNumComments(uncookedLinkDict[rawLinkGroup], True)
                
                self.bakedDict[rawLinkGroup] = temp #put the completed link group object dictionary into the final baked dict.
                
                #print(self.bakedDict[rawLinkGroup]) #diagnostic message

            
    def replaceUnicodeChars(self, ustring): # Cleans up text for UTF-8 formatting. replaces select unicode chars with their equivilent utf-8/ascii chars
        return str(ustring).replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u'\xa0', " ").replace(u"\u2013", "-").replace(u"\u201C", "\"").replace(u"\u201D", "\"")

    def __init__(self, **kwargs):
        #declare variables
        self.elementDict = dict()
        self.bakedDict = dict()

        if 'testmode' in kwargs: pass
        else:
            self.HTMLBody = self.getHTMLPage(kwargs.get('url'))
            self.parsePage(self.HTMLBody)
            self.createElementDict(self.parsedPage, self.elementDict)
            self.bakeLinkDict(self.elementDict)
        
        #Initial Diagnostics
        #print(self.linkDict.get('15786855')) # prints a test that existed in the dict on 29 Nov.
        #print(self.getHeadline(self.linkDict.get('15806500')))
        #print(self.getURL(self.linkDict.get('15807913')))
        #print('Score of this link is {}'.format(self.getPoints(self.linkDict.get('15807913'))))
        #print('Authored by: {}'.format(self.getAuthor(self.linkDict.get('15807913-data'))))
        #print('Posted {}'.format(self.getAge(self.linkDict.get('15807913-data'))))
        #print(self.getNumComments(self.linkDict.get('15807913-data'), self.linkDict.get('15807913')))
#        
        
#        print(self.parsedPage.title)
#        print(str(self.parsedPage.contents).encode('utf-8'))