# VERSION: 1.1
# AUTHORS: mauricci

from helpers import retrieve_url
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
import re

try:
    # python3
    from html.parser import HTMLParser
except ImportError:
    # python2
    from HTMLParser import HTMLParser


class cpasbien(object):
    url = "http://ww2.cpasbiens.co"
    name = 'Cpasbien (French)'
    supported_categories = {
        "all": [""],
        "books": ["ebook/"],
        "movies": ["films/"],
        "tv": ["series/"],
        "music": ["musique/"],
        "software": ["logiciels/"],
        "games": ["jeux-pc/", "jeux-consoles/"]
    }

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = "http://ww2.cpasbiens.co"
            self.TABLE_INDEX = 0
            self.insideTd = False
            self.insideDataTd = False
            self.tableCount = -1
            self.tdCount = -1
            self.fullResData = []
            self.pageRes = []
            self.singleResData = self.getSingleData()
            self.sizeFound = False
            self.seedsFound = False
            self.leechFound = False

        def getSingleData(self):
            return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def handle_starttag(self, tag, attrs):
            if tag == 'table':
                self.tableCount += 1
            if tag == 'td':
                self.insideTd = True
                Dict = dict(attrs)
                if self.tableCount == self.TABLE_INDEX:
                    self.insideDataTd = True
                    self.tdCount += 1
            if self.insideDataTd:
                Dict = dict(attrs)
                if tag == 'a' and len(attrs) > 0:
                    self.singleResData['name'] = Dict['title']
                    self.singleResData['desc_link'] = self.url + Dict['href']
                    self.singleResData['link'] = self.singleResData['desc_link']
                elif tag == 'div' and len(attrs) > 0:
                    if 'poid' in Dict.get('class', ''):
                        self.sizeFound = True
                    if 'up' in Dict.get('class', ''):
                        self.seedsFound = True
                    if 'down' in Dict.get('class', ''):
                        self.leechFound = True

        def handle_endtag(self, tag):
            if tag == 'td':
                self.insideTd = False
                self.insideDataTd = False
            if tag == 'tr':
                self.tdCount = -1
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '-1':
                        # ignore those with link and desc_link equals to -1
                        if (self.singleResData['desc_link'] != '-1' or self.singleResData['link'] != '-1'):
                            prettyPrinter(self.singleResData)
                            self.pageRes.append(self.singleResData)
                            self.fullResData.append(self.singleResData)
                    self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.insideDataTd:
                data = data.strip()
                if self.sizeFound:
                    self.singleResData['size'] = data + 'MB'
                    self.sizeFound = False
                if self.seedsFound:
                    self.singleResData['seeds'] = data
                    self.seedsFound = False
                if self.leechFound:
                    self.singleResData['leech'] = data
                    self.leechFound = False

        def feed(self, html):
            HTMLParser.feed(self, html)
            self.insideDataTd = False
            self.tdCount = -1
            self.tableCount = -1
            self.sizeFound = False
            self.seedsFound = False
            self.leechFound = False

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        parser = self.MyHTMLParser()

        # analyze firt 10 pages of results (thre are 40 entries)
        for currPage in range(1, 11):
            for subcat in currCat:
                url = '/search_torrent/{}/{}.html,page-{}' \
                    .format(subcat, what, currPage).replace('//', '/')
                url = self.url + url
                # print(url)
                html = retrieve_url(url)
                parser.feed(html)
            if len(parser.pageRes) <= 0:
                break
            del parser.pageRes[:]
        # print(parser.fullResData)
        parser.close()

    def download_torrent(self, info):
        """ Downloader """
        # download is the same file path but with different domain name
        print(info.replace(self.url, 'https://download.cpasbiens.co'))


if __name__ == "__main__":
    c = cpasbien()
    c.search('tomb%20raider')
