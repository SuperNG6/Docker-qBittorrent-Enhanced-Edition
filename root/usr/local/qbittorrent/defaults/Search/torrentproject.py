# VERSION: 1.0
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


class torrentproject(object):
    url = 'https://torrentproject2.se/'
    name = 'TorrentProject'
    supported_categories = {'all': '0'}

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'https://torrentproject2.se'
            self.insideResults = False
            self.insideDataDiv = False
            self.pageComplete = False
            self.spanCount = -1
            self.infoMap = {'name': 0, 'torrLink': 0, 'size': 5, 'seeds': 2, 'leech': 3}
            self.fullResData = []
            self.pageRes = []
            self.singleResData = self.getSingleData()

        def getSingleData(self):
            return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def handle_starttag(self, tag, attrs):
            Dict = dict(attrs)
            if tag == 'div' and 'nav' in Dict.get('id', ''):
                self.pageComplete = True
            if tag == 'div' and Dict.get('id', '') == 'similarfiles':
                self.insideResults = True
            if tag == 'div' and self.insideResults and 'gac_bb' not in Dict.get('class', ''):
                self.insideDataDiv = True
            elif tag == 'span' and self.insideDataDiv and 'verified' != Dict.get('title', ''):
                self.spanCount += 1
            if self.insideDataDiv and tag == 'a' and len(attrs) > 0:
                if self.infoMap['torrLink'] == self.spanCount and 'href' in Dict:
                    self.singleResData['link'] = self.url + Dict['href']
                if self.infoMap['name'] == self.spanCount and 'href' in Dict:
                    self.singleResData['desc_link'] = self.url + Dict['href']

        def handle_endtag(self, tag):
            if not self.pageComplete:
                if tag == 'div':
                    self.insideDataDiv = False
                    self.spanCount = -1
                    if len(self.singleResData) > 0:
                        # ignore trash stuff
                        if self.singleResData['name'] != '-1' and self.singleResData['size'] != '-1' \
                                and self.singleResData['name'].lower() != 'nome':
                            # ignore those with link and desc_link equals to -1
                            if self.singleResData['desc_link'] != '-1' or self.singleResData['link'] != '-1':
                                try:
                                    prettyPrinter(self.singleResData)
                                except:
                                    print(self.singleResData)
                                self.pageRes.append(self.singleResData)
                                self.fullResData.append(self.singleResData)
                        self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.insideDataDiv:
                for key, val in self.infoMap.items():
                    if self.spanCount == val:
                        currKey = key
                        if currKey in self.singleResData and data.strip() != '':
                            if self.singleResData[currKey] == '-1':
                                self.singleResData[currKey] = data.strip()
                            elif currKey != 'name':
                                self.singleResData[currKey] += data.strip()

        def feed(self, html):
            HTMLParser.feed(self, html)
            self.pageComplete = False
            self.insideResults = False
            self.insideDataDiv = False
            self.spanCount = -1

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        parser = self.MyHTMLParser()
        what = what.replace('%20', '+')
        # analyze firt 10 pages of results
        for currPage in range(0, 10):
            url = self.url + '?t={0}&p={1}'.format(what, currPage)
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
        print(download_file(info))


if __name__ == "__main__":
    t = torrentproject()
    t.search('tomb%20raider')
