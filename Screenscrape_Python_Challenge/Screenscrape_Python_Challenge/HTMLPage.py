import asyncio, asyncore, argparse, urllib.request, http

class HTMLPage:
    """Creates an HTML object that can be navigated"""

    def getHTMLPage(self, url): # Gets an HTTP(s) page and returns an HTML object
        try:
            self.html = urllib.request.urlopen(url)
            print('we seem to have successfully retrieved {}'.format(url))
            return self.html
        except Exception as e:
            print(e)

    def GetProperty(self, args):
        return self.args[0]


    def __init__(self, **kwargs):
        self.HTMLBody = self.getHTMLPage(kwargs.get('url'))
        
