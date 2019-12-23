# VERSION: 1.6
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


class corsaronero(object):
    url = 'http://ilcorsaroneros.info'
    name = 'Il Corsaro Nero'
    supported_categories = {'all': '0'}

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'http://ilcorsaroneros.info'
            self.TABLE_INDEX = 4
            self.insideTd = False
            self.insideDataTd = False
            self.tableCount = -1
            self.tdCount = -1
            self.infoMap = {'name': 1, 'size': 2, 'seeds': 5, 'leech': 6}
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
                self.insideTd = True
                Dict = dict(attrs)
                if self.tableCount == self.TABLE_INDEX:
                    self.insideDataTd = True
                    self.tdCount += 1
            if self.insideDataTd and tag == 'a' and len(attrs) > 0:
                Dict = dict(attrs)
                if self.infoMap['name'] == self.tdCount and 'href' in Dict:
                    self.singleResData['desc_link'] = Dict['href']
                    self.singleResData['link'] = self.singleResData['desc_link']

        def handle_endtag(self, tag):
            if tag == 'td':
                self.insideTd = False
                self.insideDataTd = False
            if tag == 'tr':
                self.tdCount = -1
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '-1' and self.singleResData['size'].find(',') == -1:
                        # ignore those with link and desc_link equals to -1
                        if (self.singleResData['desc_link'] != '-1' or self.singleResData['link'] != '-1'):
                            self.adjustName()
                            prettyPrinter(self.singleResData)
                            self.pageRes.append(self.singleResData)
                            self.fullResData.append(self.singleResData)
                    self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.insideDataTd:
                # print(data)
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

        def adjustName(self):
            name = self.singleResData.get('name', '')
            # if name ends with .. then we remove the 2 ending dots
            if name.endswith('..'):
                self.singleResData['name'] = name[:-2]

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        parser = self.MyHTMLParser()

        # analyze firt page of results (thre are 40 entries)
        for currPage in range(1, 2):
            url = self.url + '/argh.php?search={0}&page={1}'.format(what, currPage)
            #print(url)
            html = retrieve_url(url)
            parser.feed(html)
            if len(parser.pageRes) <= 0:
                break
            del parser.pageRes[:]
        # print(parser.fullResData)
        data = parser.fullResData
        parser.close()

    def download_torrent(self, info):
        """ Downloader """
        html = retrieve_url(info)
        m = re.search('(<a.*? class=".*?magnet".*?>)', html)
        if m and len(m.groups()) > 0:
            magnetAnchor = m.group(1)
            if magnetAnchor:
                magnetLink = re.search('href="(.+?)"', magnetAnchor)
                if magnetLink and len(magnetLink.groups()) > 0:
                    print(magnetLink.group(1) + ' ' + info)


if __name__ == "__main__":
    c = corsaronero()
    c.search('tomb%20raider')
