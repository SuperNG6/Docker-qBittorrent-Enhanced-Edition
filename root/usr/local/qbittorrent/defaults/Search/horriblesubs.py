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


class horriblesubs(object):
    url = 'https://horriblesubs.info/'
    name = 'Horriblesubs'
    supported_categories = {
        "all": "0"
    }

    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'https://horriblesubs.info/'
            self.fullResData = []
            self.pageRes = []
            self.singleResData = self.getSingleData()
            self.resetVars()

        def resetVars(self):
            self.titleFound = False
            self.tagCount = -1

        def getSingleData(self):
            return {'name': '', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                    'engine_url': self.url}

        def handle_starttag(self, tag, attrs):
            Dict = dict(attrs)
            if self.titleFound:
                self.tagCount += 1
            if tag == 'a' and 'href' in Dict:
                self.titleFound = True
                self.singleResData['desc_link'] = self.url + Dict['href']
                self.singleResData['link'] = self.singleResData['desc_link']

        def handle_endtag(self, tag):
            if tag == 'li':
                self.titleFound = False
                self.tagCount = -1
                if len(self.singleResData) > 0:
                    # ignore trash stuff
                    if self.singleResData['name'] != '':
                        # ignore those with desc_link equals to -1
                        if self.singleResData['desc_link'] != '-1':
                            # remove trash from name
                            self.singleResData['name'] = self.clearName(self.singleResData['name'])
                            prettyPrinter(self.singleResData)
                            self.pageRes.append(self.singleResData)
                            self.fullResData.append(self.singleResData)
                    self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.titleFound:
                data = data.strip()
                if self.tagCount == 0 or self.tagCount == 1:
                    self.singleResData['name'] += data

        def feed(self, html):
            HTMLParser.feed(self, html)
            self.resetVars()

        def clearName(self, name):
            # this could be the name '01/19/19Sword Art Online - Alicization - 15'
            # removing date info
            return re.sub(r'(^[yY]esterday)|(^\d+/\d+/\d+)', '', name)

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        what = what.replace('%20', '+')
        parser = self.MyHTMLParser()
        beforeLength = -1
        # analyze firt 10 pages of results
        for currPage in range(0, 10):
            url = 'api.php?method=search&value={0}&nextid={1}' \
                .format(what, currPage)
            url = self.url + url
            # print(url)
            html = retrieve_url(url)
            parser.feed(html)
            if len(parser.pageRes) <= 0:
                break
            del parser.pageRes[:]
        # print(parser.fullResData)
        parser.close()


if __name__ == "__main__":
    h = horriblesubs()
    h.search('sword%20art&20online')
