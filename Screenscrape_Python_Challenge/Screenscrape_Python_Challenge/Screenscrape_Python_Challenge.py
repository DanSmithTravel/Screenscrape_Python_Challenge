# Screenscrape Python Challenge
# Developed by Daniel Smith
# This application will scrape html element data from https://news.ycombinator.com/ and collate that data into a local text file.

import asyncio, asyncore, argparse, urllib.request, http
from HTMLPage import HTMLPage
from bs4 import BeautifulSoup

def main():
        page = HTMLPage(url = 'https://news.ycombinator.com/')
                
    

if __name__ == '__main__': main()
