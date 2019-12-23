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


class foxcili(object):
    url = 'http://foxcili.org/'
    name = 'Foxcili'
    supported_categories = {
        "all": "0",
        "books": "0",
        "movies": "2",
        "tv": "0",
        "music": "3",
        "software": "5",
        "games": "0"
    }

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'http://foxcili.org/'
            self.fullResData = []
            self.singleResData = self.getSingleData()
            self.resetVars()

        def resetVars(self):
            self.titleFound = False
            self.insideSBar = False
            self.spanCount = -1
            self.currAttrsList = []

        def getSingleData(self):
            return {'name': '', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def handle_starttag(self, tag, attrs):
            Dict = dict(attrs)
            self.currAttrsList.append(Dict)
            if tag == 'div' and Dict.get('class', '') == 'title':
                self.titleFound = True

            if self.titleFound:
                if self.singleResData['desc_link'] == '-1' and tag == 'a' and 'href' in Dict:
                    self.singleResData['desc_link'] = Dict['href']

            if tag == 'div' and 'sbar' in Dict.get('class', ''):
                self.insideSBar = True

            if self.insideSBar and tag == 'span':
                self.spanCount += 1

            if tag == 'a' and 'magnet' in Dict.get('href', ''):
                self.singleResData['link'] = Dict['href']

        def handle_endtag(self, tag):
            currTagAttrs = self.currAttrsList.pop()
            if tag == 'div':
                self.spanCount = -1
            if tag == 'div' and 'ssbox' == currTagAttrs.get('class', ''):
                self.insideSBar = False
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '':
                        # ignore those withdesc_link equals to -1
                        if self.singleResData['desc_link'] != '-1':
                            prettyPrinter(self.singleResData)
                            self.fullResData.append(self.singleResData)
                    self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.titleFound or self.insideSBar:
                data = data.strip()
                self.singleResData['name'] += self.clearName(data)
                if self.spanCount == 1:  # 1 = size's span index
                    sCleared = self.clearSize(data)
                    if self.singleResData['size'] == '-1' and sCleared != '-1':
                        self.singleResData['size'] = sCleared

        def feed(self, html):
            HTMLParser.feed(self, html)
            self.resetVars()

        def clearName(self, name):
            return re.sub(r'\[.*?\]', '', name)

        def clearSize(self, size):
            m = re.search(r'(\d.*)', size)
            return m.group(0) if m else '-1'

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        parser = self.MyHTMLParser()

        # analyze firt 10 pages of results (thre are 40 entries)
        for currPage in range(1, 11):
            url = 'fox/{1}/{2}/0/{0}.html' \
                .format(currCat, what, currPage)
            url = self.url + url
            # print(url)
            html = retrieve_url(url)
            parser.feed(html)
            if len(parser.fullResData) <= 0:
                break
        # print(parser.fullResData)
        parser.close()


if __name__ == "__main__":
    f = foxcili()
    f.search('tomb%20raider')
