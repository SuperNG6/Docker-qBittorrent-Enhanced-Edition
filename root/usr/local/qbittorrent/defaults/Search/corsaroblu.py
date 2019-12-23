# VERSION: 1.7
# AUTHORS: mauricci

from helpers import retrieve_url
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter

try:
    # python3
    from html.parser import HTMLParser
except ImportError:
    # python2
    from HTMLParser import HTMLParser


class corsaroblu(object):
    url = 'https://www.ilcorsaroblu.org/'
    name = 'Il Corsaro Blu'
    # 13%3B14%3B15%3B25%3B17%3B11%3B21 = 13;14;15;25;17;11;21
    supported_categories = {'all': '0', 'movies': '13%3B14%3B15%3B25%3B17%3B11%3B21', 'tv': '19%3B20%3B24',
                            'music': '2', 'games': '3'}

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'https://www.ilcorsaroblu.org/'
            self.TABLE_INDEX = 9
            self.insideDataTd = False
            self.tableCount = -1
            self.tdCount = -1
            self.infoMap = {'name': 1, 'torrLink': 3, 'size': 8, 'seeds': 6, 'leech': 7}
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
                Dict = dict(attrs)
                if self.tableCount == self.TABLE_INDEX:
                    self.insideDataTd = True
                    self.tdCount += 1
            if self.insideDataTd and tag == 'a' and len(attrs) > 0:
                Dict = dict(attrs)
                if self.infoMap['torrLink'] == self.tdCount and 'href' in Dict:
                    self.singleResData['link'] = self.url + Dict['href']
                if self.infoMap['name'] == self.tdCount and 'href' in Dict:
                    self.singleResData['desc_link'] = self.url + Dict['href']

        def handle_endtag(self, tag):
            if tag == 'td':
                self.insideDataTd = False
            if tag == 'tr':
                self.tdCount = -1
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '-1' and self.singleResData['size'].find(',') == -1 \
                            and self.singleResData['name'].lower() != 'nome':
                        # ignore those with link and desc_link equals to -1
                        if (self.singleResData['desc_link'] != '-1' or self.singleResData['link'] != '-1'):
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
            url = self.url + 'index.php?page=torrents&search={0}&category={1}&pages={2}'.format(what, currCat,
                                                                                                 currPage)
            # print(url)
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
        print(download_file(info))


if __name__ == "__main__":
    c = corsaroblu()
    c.search('tomb%20raider')
