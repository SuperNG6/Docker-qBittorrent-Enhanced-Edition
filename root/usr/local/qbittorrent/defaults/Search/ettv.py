#VERSION: 1.1
#AUTHORS: mauricci

from helpers import retrieve_url
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
import re

try:
    #python3
    from html.parser import HTMLParser
except ImportError:
    #python2
    from HTMLParser import HTMLParser
         
class ettv(object):
    url = 'https://www.ettv.tv'
    name = 'ETTV'
    supported_categories = {'all': '0'}
    
    class MyHTMLParser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.url = 'https://www.ettv.tv'
            self.TABLE_INDEX = 1
            self.insideDataTd = False
            self.tdCount = -1
            self.tableCount = -1
            self.infoMap = {'name':1,'size':3,'seeds':5,'leech':6}
            self.fullResData = []
            self.singleResData = self.getSingleData()
            
        def getSingleData(self):
            return {'name':'-1','seeds':'-1','leech':'-1','size':'-1','link':'-1','desc_link':'-1','engine_url':self.url}
        
        def handle_starttag(self, tag, attrs):
            #print("Encountered a start tag:", tag)
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
                    #ignore trash stuff
                    if self.singleResData['name'] != '-1' \
                        and self.isValidSize(self.singleResData['size']):
                        self.fixSeedOrLeechNumber(self.singleResData)
                        prettyPrinter(self.singleResData)
                        self.fullResData.append(self.singleResData)
                    self.singleResData = self.getSingleData()

        def handle_data(self, data):
            if self.insideDataTd:
                for key,val in self.infoMap.items():
                    if self.tdCount == val:
                        currKey = key
                        if currKey in self.singleResData and data.strip() != '':
                            if self.singleResData[currKey] == '-1':
                                self.singleResData[currKey] = data.strip()
                            else:
                                self.singleResData[currKey] += data.strip()

        def feed(self,html):
            HTMLParser.feed(self,html)
            self.insideDataTd = False
            self.tdCount = -1
            self.tableCount = -1
            
        #true if the size is valid (mustn't contain 'n/a' or commas)
        def isValidSize(self, size):
            return not bool(re.search(r'(?:n/a)|(?:\,)', str(size).lower()))
        
        #seed and leech number greater than 999 are separeted by comma
        #prettyPrinter wants them without comma, so we remove it
        def fixSeedOrLeechNumber(self,Dict):
            for key in ['seeds','leech']:
                if Dict[key].count(',') == 1:
                    Dict[key] = Dict[key].replace(',','')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        currCat = self.supported_categories[cat]
        what = what.replace('%20','+')
        parser = self.MyHTMLParser()
        #analyze firt 10 pages of results
        for currPage in range(0,10):
            url = self.url+'/torrents-search.php?search={0}&sort=seeders&cat={1}&order=desc&page={2}' \
                  .format(what,currCat,currPage)
            print(url)
            html = retrieve_url(url)
            parser.feed(html)
            if len(parser.fullResData) <= 0:
                break
        #print(parser.fullResData)   
        data = parser.fullResData
        parser.close()

    def download_torrent(self, info):
        """ Downloader """
        html = retrieve_url(info)
        m = re.search('<a\s?href=[\'\"](magnet\:\?.+?)[\'\"]', html)
        if m and len(m.groups()) > 0:
            print(m.group(1) + ' ' + info)

if __name__ == "__main__":
    e = ettv()
    e.search('tomb%20raider')
