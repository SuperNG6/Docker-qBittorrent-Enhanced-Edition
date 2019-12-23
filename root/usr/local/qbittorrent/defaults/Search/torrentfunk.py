# VERSION: 1.0
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


class torrentfunk(object):
    url = 'https://www.torrentfunk2.com'
    name = 'TorrentFunk'
    supported_categories = {'all': 'all', 'movies': 'movie', 'tv': 'television', 'music': 'music', 'games': 'games',
                            'anime': 'anime', 'software': 'software'}

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'https://www.torrentfunk2.com'
            self.TABLE_INDEX = 6
            self.insideDataTd = False
            self.tdCount = -1
            self.tableCount = -1
            self.infoMap = {'name': 0, 'size': 2, 'seeds': 3, 'leech': 4}
            self.fullResData = []
            self.singleResData = self.getSingleData()

        def getSingleData(self):
            return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def handle_starttag(self, tag, attrs):
            # print("Encountered a start tag:", tag)
            if tag == 'table':
                self.tableCount += 1
            if tag == 'td':
                self.tdCount += 1
                if self.tableCount == self.TABLE_INDEX:
                    self.insideDataTd = True
            if self.insideDataTd and tag == 'a' and len(attrs) > 0:
                Dict = dict(attrs)
                if self.infoMap['name'] == self.tdCount and 'href' in Dict:
                    self.singleResData['desc_link'] = self.url + Dict['href']
                    self.singleResData['link'] = self.singleResData['desc_link']

        def handle_endtag(self, tag):
            if tag == 'td':
                self.insideDataTd = False
            if tag == 'tr':
                self.tdCount = -1
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '-1' and \
                            not self.singleResData['name'].lower().startswith('torrent name'):
                        prettyPrinter(self.singleResData)
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

    def download_torrent(self, info):
        html = retrieve_url(info)
        m = re.search('(/tor/.+?\s)', html)
        if m and len(m.groups()) > 0:
            print(download_file(self.url + m.group(1)))

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        what = what.replace('%20', '-')
        parser = self.MyHTMLParser()
        # analyze firt page with 250 results
        for currPage in range(1, 2):
            url = self.url + '/{0}/torrents/{1}.html?sort=seed&o=desc&i=250'.format(currCat, what, currPage)
            print(url)
            html = retrieve_url(url)
            parser.feed(html)
            if len(parser.fullResData) <= 0:
                break
        # print(parser.fullResData)
        data = parser.fullResData
        parser.close()


if __name__ == "__main__":
    t = torrentfunk()
    t.search('tomb%20raider')
