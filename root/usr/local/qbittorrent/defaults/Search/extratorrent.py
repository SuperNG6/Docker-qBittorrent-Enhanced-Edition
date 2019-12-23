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


class extratorrent(object):
    url = 'https://extratorrent.si'
    name = 'ExtraTorrent'
    supported_categories = {'all': '0', 'movies': '4', 'tv': '8', 'music': '5', 'games': '3', 'anime': '1',
                            'software': '7'}

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'https://extratorrent.si'
            self.TABLE_INDEX = 13
            self.insideDataTd = False
            self.tdCount = -1
            self.tableCount = -1
            self.infoMap = {'torrLink': 0, 'name': 2, 'size': 4, 'seeds': 5, 'leech': 6}
            self.fullResData = []
            self.pageRes = []
            self.singleResData = self.getSingleData()

        def getSingleData(self):
            return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def handle_starttag(self, tag, attrs):
            if tag == 'table':
                self.tableCount += 1
            if tag == 'td':
                self.tdCount += 1
                if self.tableCount == self.TABLE_INDEX:
                    self.insideDataTd = True
            if self.insideDataTd and tag == 'a' and len(attrs) > 0:
                Dict = dict(attrs)
                if self.tdCount == self.infoMap['torrLink']:
                    if Dict.get('href', '').startswith('magnet'):
                        self.singleResData['link'] = Dict['href']
                    if Dict.get('href', '').find('extratorrent') != -1:
                        if Dict['href'].startswith('//'):
                            Dict['href'] = Dict['href'].replace('//extratorrent.si', self.url)
                        self.singleResData['desc_link'] = Dict['href']

        def handle_endtag(self, tag):
            if tag == 'td':
                self.insideDataTd = False
            if tag == 'tr':
                self.tdCount = -1
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '-1':
                        prettyPrinter(self.singleResData)
                        self.pageRes.append(self.singleResData)
                        self.fullResData.append(self.singleResData)
                    self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.insideDataTd:
                for key, val in self.infoMap.items():
                    if self.tdCount == val:
                        currKey = key
                        if currKey in self.singleResData and data.strip() != '':
                            if self.singleResData[currKey] == '-1':
                                self.singleResData[currKey] = data.strip()
                            else:
                                self.singleResData[currKey] += data.strip()

        def feed(self, html):
            HTMLParser.feed(self, html)
            self.insideDataTd = False
            self.tdCount = -1
            self.tableCount = -1

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        parser = self.MyHTMLParser()

        # analyze firt 10 pages of results
        for currPage in range(1, 11):
            url = self.url + '/search/?search={0}&page={1}&s_cat={2}'.format(what, currPage, currCat)
            # print(url)
            html = retrieve_url(url)
            parser.feed(html)
            if len(parser.pageRes) <= 0:
                break
            del parser.pageRes[:]
        #print(parser.fullResData[0])
        data = parser.fullResData
        parser.close()


if __name__ == "__main__":
    e = extratorrent()
    e.search('tomb%20raider')
