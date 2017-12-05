import io, asyncio, asyncore, argparse, urllib.request, http, re, unicodedata, time, aiohttp, async_timeout, threading
from threading import current_thread
from bs4 import BeautifulSoup

class HTMLPage:
    """Creates an HTML object that can be navigated\r
    Pass in testmode(any value) and testmodeFile(local HTML file) to run object in testing mode with local HTML from file.\r
    In testmode, also pass in localexec(any value) to go ahead and automatically run the init methods with the passed file."""


    async def getHTMLPage(self, url = None, testmode = False, testmodeFile = ''):
        """Gets an HTTP(s) page and returns an HTML object\r
        Pass in url only for live mode.\r
        Pass in testmode(any value) and testmodeFile(local HTML file) for testing."""
        
        if testmode: #
            try:
                return open(testmodeFile, encoding = 'utf-8')

            except Exception as e:
                print(e)

        elif url != '':
            try:
                #return urllib.request.urlopen(url)
                
                async with aiohttp.ClientSession() as session:
                    html = await self.fetchPage(session, url, 5)
                    return html
            
            except Exception as e:
                print(e)
        else:
            raise Exception("No URL passed in live mode. Cannot retrieve any page.")


    async def fetchPage(self, session, url, timeout = 10):
        with async_timeout.timeout(timeout):
            async with session.get(url) as response:
                return await response.text()

    async def parsePage(self, HTMLBody, testmode = False):
        """parses the HTML body into a BeautifulSoup object."""
        
        try:
            self.parsedPage = BeautifulSoup(HTMLBody.read() if testmode else HTMLBody, 'html.parser')
        except Exception as e:
            print('There was an error trying to parse the page. Error:\n{}'.format(e)) #Diagnostic message

    def createElementDict(self, parsedPage, dictionary): 
        """create a dictionary of all link groups on the HTML page"""
                
        #print('trying...') #Diagnostic message
        for element in parsedPage.find_all('tr'): #search and gather all 'athing' elements in the page. This are the containers for each link.
            #print('trying to iterate...') #Diagnostic message
            try:
                if 'athing' in element.get('class'): # a link group in the HTML has the class 'athing' skip all others.
                    element.append(element.next_sibling) #combine main link element group with the next one that contains additional properties like score.
                    id = element.attrs['id']
                    dictionary[id] = element    #set the key/value  pair in the dictionary to [uniqueID : data object]

            except Exception as e:
                #diagnostic
                pass 

    def getHeadline(self, element):
        """find the 'storylink' in the given link group element. Extract the headline text."""
        #print(element) #Diagnostic message
        for tag in element.find_all('a'):
            try:
                if 'storylink' in tag.get('class'):
                    #print('found a link') #Diagnostic message
                    return self.replaceUnicodeChars(tag.next_element)

            except Exception as e:
                #print(e)    
                pass
    
    def getURL(self, element):
        """Search through all <a> tags in the link group element. Extract the URL that corresponds to the headline text."""
        
        for tag in element.find_all('a'):
            try:
                if 'storylink' in tag.get('class'):
                    #print('found a link')  #diagnostic message
                    return tag.get('href')

            except:
                pass

    def getPoints(self, element, trim = True):
        """Search through all <span> tags in the link group element for the 'score' class. Extract the number of points."""

        for tag in element.find_all('span'):
            try:
                if 'score' in tag.get('class'):
                    if trim: return re.search('\\d+', tag.next_element).group(0)
                    else: return tag.next_element

            except:
                pass
    
    def getAuthor(self, element):
        """#Search through all <a> tags in the link group element and find the 'hnuser' class and extract the submitters username.\r
        This method can return None if the story was submitted anonymously."""
        for tag in element.find_all('a'):
            try:
                if 'hnuser' in tag.get('class'):
                    return tag.next_element
            except:
                pass

    def getAge(self, element, trim=False, minutesOnly = True):
        """Returns age of post in 'xx minutes/hours/days ago'.\r
        If trim=True, method returns a flat digit value."""
        for tag in element.find_all('span'):
            try:
                if 'age' in tag.get('class'):
                    if trim:
                        return re.search('\\d+', tag.next_element.next_element).group(0) #returns just the first group of digits in the string, i.e. the number of hours/minutes
                    elif minutesOnly:
                        if 'minutes' in tag.next_element.next_element: return re.search('\\d+', tag.next_element.next_element).group(0)
                        elif 'hours' in tag.next_element.next_element: return str(int(re.search('\\d+', tag.next_element.next_element).group(0)) * 60)
                        elif 'days' or 'day' in tag.next_element.next_element: return str(int(re.search('\\d+', tag.next_element.next_element).group(0)) * 60 * 24)
                        else: return None
                        
                    else: return tag.next_element.next_element

            except:
                pass

    def getNumComments(self, element, trim=False):
        """Search through all <a href> tags in the link group element and find the one that includes the word 'comments' in the link display text.\r
        If trim=True, method returns a flat digit value.\r
        This method can return None if no one has commented on the story."""
        for tag in element.find_all('a'):
            try:
               if element.attrs['id'] in tag.get('href') and 'comments' in tag.next_element:
                   if trim: return str.replace(tag.next_element,'\xa0comments', "") 
                   else: return str(str.replace(tag.next_element,'\xa0', " ")).encode('utf-8')

            except:
                pass

    def getRank(self, element):
        for tag in element.find_all('span'):
            try:
                if 'rank' in tag.get('class'):
                    return re.search('\\d+', tag.next_element).group(0)
                    #else: return tag.next_element

            except:
                pass

    def bakeLinkDict(self, uncookedLinkDict):
        """#Assembles a dictionary of formatted name/value pairs for relevant link information."""
        
        for rawLinkGroup in uncookedLinkDict:
                temp = dict() # Put all the local data into a temporary dictionary to group it.
                temp['id'] = rawLinkGroup
                temp['headline'] = self.getHeadline(uncookedLinkDict[rawLinkGroup])
                temp['rank'] = self.getRank(uncookedLinkDict[rawLinkGroup])
                temp['URL'] = self.getURL(uncookedLinkDict[rawLinkGroup]) # Makes diag output difficult to read. Re-enable later.
                temp['score'] = self.getPoints(uncookedLinkDict[rawLinkGroup])
                temp['author'] = self.getAuthor(uncookedLinkDict[rawLinkGroup])
                temp['age'] = self.getAge(uncookedLinkDict[rawLinkGroup], minutesOnly = True)
                temp['comments'] = self.getNumComments(uncookedLinkDict[rawLinkGroup], True)
                # Put the completed link group object dictionary into the final baked dict.
                self.bakedDict[rawLinkGroup] = temp
            
    def replaceUnicodeChars(self, ustring):
        """Cleans up text for UTF-8 formatting. replaces select unicode chars with their equivilent utf-8/ascii chars"""
        return str(ustring).replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u'\xa0', " ").replace(u"\u2013", "-").replace(u"\u201C", "\"").replace(u"\u201D", "\"")

    def __init__(self, **kwargs):
        #initialize variables and print diagnostic trace
        self.startTime = time.time()
        self.elementDict = dict()
        self.bakedDict = dict()
        
        try:
            self.URL = kwargs['url'] # See if we're in testmode or not and pull the URL if we are.
            print('HTMLPage Object {} created at {}\n'.format(self.URL, time.time()))
        except Exception as e:
            print('No URL passed. we might be in testmode.\nTestmode: {}'.format('testmode' in kwargs))
            if 'testmode' not in kwargs: raise Exception('Error: No URL passed to object, but we\'re not in test mode!. Exception:\n{}'.format(e))
            else: pass # test for testmode below.

        
        if 'testmode' in kwargs: # if testmode(any value) was passed in, run object in testing mode with local HTML from file.
            print('HTMLPage Object {} created at {}\n'.format(kwargs.get('testmodeFile'), time.time()))
            if 'localexec' in kwargs: # if localexec(any value) was passed in, go ahead and automatically run the init methods with the passed file.
                loop = asyncio.new_event_loop() # generate a new loop in case we're already executing in one.
                asyncio.set_event_loop(loop) # set the new loop
                
                # get the HTML page in async testmode
                loop.run_until_complete(
                    asyncio.gather(self.process_async_HTMLBody(self.getHTMLPage, testmode = True, testmodeFile = kwargs['testmodeFile']))
                                )
                loop.run_until_complete(self.parsePage(self.HTMLBody)) # parse the page async
                loop.close() # loop no longer needed. close it.

                self.createElementDict(self.parsedPage, self.elementDict) # create a dictionary of the link group objects from the page
                self.bakeLinkDict(self.elementDict) # bake the link dict into plain text for printing
            else:
                pass

        else: # assume this is a live execute and NOT in testmode or running unit tests
            pass

    
        
    def manualInit(self):
        '''Build out object, including HTTP request and baking the link dictionary.'''
        manInitTime = time.time()
        print('Starting manual init of: {} on thread {} at {}\n'.format(self.URL, current_thread(), manInitTime))
        
        loop = asyncio.new_event_loop() # generate a new loop in case we're already executing in one.
        asyncio.set_event_loop(loop) # set the new loop
        loop.run_until_complete(
            asyncio.gather(self.process_async_HTMLBody(self.getHTMLPage))
                                )    
        loop.run_until_complete(self.parsePage(self.HTMLBody)) # parse the page async
        loop.close() # loop no longer needed. close it.

        self.createElementDict(self.parsedPage, self.elementDict) # create a dictionary of the link group objects from the page
        self.bakeLinkDict(self.elementDict) # bake the link dict into plain text for printing
        print('Finished async manual init of: {} at {}.\n It took {:.2f} seconds'.format(self.URL, time.time(), time.time() - manInitTime))

        return self
        
    async def process_async_HTMLBody(self, async_function, testmode = False, testmodeFile = None):
        if testmode:
            self.HTMLBody = await async_function(testmode = testmode, testmodeFile = testmodeFile)
        else:
            self.HTMLBody = await async_function(url = self.URL)
        return    
