#VERSION: 0.03
#AUTHORS: nindogo

import threading
import logging
import time
import urllib
import codecs
import ssl
import tempfile

# logging.basicConfig(level=logging.INFO,
#     format='%(asctime)s:%(levelname)s:%(filename)s:%(threadName)s:%(lineno)d:%(message)s')
# logging.getLogger(__name__)

import re

#qbt
from helpers import retrieve_url
from novaprinter import prettyPrinter

class unionDHTParser(threading.Thread):
    page_link = threading.local()
    # page_content = threading.local()
    # the_page_results = threading.local()
    each_result = threading.local()
    b = threading.local()

    SEE_ALL = re.compile(r'tLink"\s+?href="(.+?)"><b>(.*?)<\/b>.+?tr-dl" href="(.+?)">(.+?)<\/a>.+?seedmed bold">(\d)<\/td>.+?leechmed" title="Личеров"><b>(\d)',re.S)

    def __init__(self, url):
        logging.info('Initiating Parser')
        self.page_link = url
        threading.Thread.__init__(self)
        logging.info('Parser Initiation complete')
    
    def get_page_data(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0')
        with urllib.request.urlopen(req) as response:
            html = response.read()
            new_html = codecs.decode(html, encoding='cp1251')
            return(new_html)
        

    def run(self):
        logging.info('Starting unionDHTParser Thread')
        logging.debug('Current link is {}'.format(self.page_link))
        page_content = self.get_page_data(self.page_link)
        logging.debug('Thread data: {}'.format(page_content))
        the_page_results = re.findall(self.SEE_ALL, page_content)
        logging.debug(the_page_results)

        for self.each_result in the_page_results:
            logging.debug('Preparing to PrettyPrint {}'.format(self.each_result[1]))
            self.b = dict()
            self.b['desc_link'] = 'http://uniondht.org' + self.each_result[0]
            self.b['name'] = self.each_result[1].replace('<wbr>','')
            self.b['link'] = '' #'http://uniondht.org' + self.each_result[2]
            self.b['size'] = self.each_result[3].replace(' ', '').replace('&nbsp;', ' ')
            self.b['seeds'] = self.each_result[4]
            self.b['leech'] = self.each_result[5]
            self.b['engine_url'] = 'http://uniondht.org'
            logging.debug('ready to prettyPrint record: {}'.format(self.b['name']))
            prettyPrinter(self.b)

            self.b.clear()

def get_page_data(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0')
    ctx = ssl.SSLContext()
    # ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req,context=ctx) as response:
        new_html = response.read().decode('cp1251')
        # print((new_html))
        # print(type(html))
        # new_html = codecs.decode(html, encoding='cp1251')
        # new_html = html.decode('cp1251')
        return(new_html)

def get_page_data_encoded(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0')
    ctx = ssl.SSLContext()
    # ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req,context=ctx) as response:
        new_html = response.read()
        # print(type(html))
        # new_html = codecs.decode(html, encoding='cp1251')
        # new_html = html.decode('cp1251')
        return(new_html)
class uniondht(object):
    logging.info('Class Starting')
    supported_categories = {'all': ''
                            , 'books': '&f%5B%5D=810&f%5B%5D=812&f%5B%5D=813&f%5B%5D=818&f%5B%5D=826&f%5B%5D=910&f%5B%5D=817&f%5B%5D=816&f%5B%5D=815&f%5B%5D=814&f%5B%5D=811&f%5B%5D=825&f%5B%5D=824&f%5B%5D=823&f%5B%5D=822&f%5B%5D=820&f%5B%5D=819'
                            , 'anime': '&f%5B%5D=211&f%5B%5D=517&f%5B%5D=518&f%5B%5D=928&f%5B%5D=929&f%5B%5D=930&f%5B%5D=519&f%5B%5D=520&f%5B%5D=212&f%5B%5D=230&f%5B%5D=521&f%5B%5D=214&f%5B%5D=226&f%5B%5D=225'
                            , 'software': '&f%5B%5D=238&f%5B%5D=371&f%5B%5D=370&f%5B%5D=369&f%5B%5D=368&f%5B%5D=367&f%5B%5D=366&f%5B%5D=365&f%5B%5D=239&f%5B%5D=361&f%5B%5D=360&f%5B%5D=359&f%5B%5D=241&f%5B%5D=349&f%5B%5D=348&f%5B%5D=347&f%5B%5D=346&f%5B%5D=939&f%5B%5D=1132&f%5B%5D=345&f%5B%5D=344&f%5B%5D=242&f%5B%5D=340&f%5B%5D=339&f%5B%5D=338&f%5B%5D=337&f%5B%5D=336&f%5B%5D=335&f%5B%5D=334&f%5B%5D=333&f%5B%5D=332&f%5B%5D=331&f%5B%5D=330&f%5B%5D=329&f%5B%5D=328&f%5B%5D=327&f%5B%5D=326&f%5B%5D=243&f%5B%5D=324&f%5B%5D=323&f%5B%5D=322&f%5B%5D=321&f%5B%5D=320&f%5B%5D=319&f%5B%5D=318&f%5B%5D=317&f%5B%5D=316&f%5B%5D=315&f%5B%5D=314&f%5B%5D=313&f%5B%5D=312&f%5B%5D=311&f%5B%5D=244&f%5B%5D=307&f%5B%5D=306&f%5B%5D=305&f%5B%5D=304&f%5B%5D=303&f%5B%5D=302&f%5B%5D=301&f%5B%5D=245&f%5B%5D=297&f%5B%5D=296&f%5B%5D=295&f%5B%5D=294&f%5B%5D=293&f%5B%5D=292&f%5B%5D=291&f%5B%5D=290&f%5B%5D=289&f%5B%5D=288&f%5B%5D=287&f%5B%5D=246&f%5B%5D=284&f%5B%5D=283&f%5B%5D=282&f%5B%5D=281&f%5B%5D=280&f%5B%5D=1129&f%5B%5D=278&f%5B%5D=277&f%5B%5D=276&f%5B%5D=275&f%5B%5D=274&f%5B%5D=247&f%5B%5D=272&f%5B%5D=271&f%5B%5D=270&f%5B%5D=248&f%5B%5D=1047&f%5B%5D=1048&f%5B%5D=268&f%5B%5D=267&f%5B%5D=266&f%5B%5D=265&f%5B%5D=1046&f%5B%5D=263&f%5B%5D=249&f%5B%5D=715&f%5B%5D=262&f%5B%5D=260&f%5B%5D=259&f%5B%5D=258&f%5B%5D=257&f%5B%5D=250&f%5B%5D=254&f%5B%5D=253&f%5B%5D=251'
                            , 'movies': '&f%5B%5D=783&f%5B%5D=197&f%5B%5D=1142&f%5B%5D=1131&f%5B%5D=198&f%5B%5D=155&f%5B%5D=784&f%5B%5D=184&f%5B%5D=158&f%5B%5D=924&f%5B%5D=172&f%5B%5D=830&f%5B%5D=1128&f%5B%5D=832&f%5B%5D=833&f%5B%5D=834&f%5B%5D=187&f%5B%5D=156&f%5B%5D=157&f%5B%5D=159&f%5B%5D=160&f%5B%5D=161&f%5B%5D=695&f%5B%5D=1124&f%5B%5D=922&f%5B%5D=931&f%5B%5D=1130&f%5B%5D=737&f%5B%5D=987&f%5B%5D=748&f%5B%5D=747&f%5B%5D=743&f%5B%5D=742&f%5B%5D=741&f%5B%5D=739&f%5B%5D=738'
                            , 'music': '&f%5B%5D=574&f%5B%5D=595&f%5B%5D=594&f%5B%5D=593&f%5B%5D=592&f%5B%5D=591&f%5B%5D=590&f%5B%5D=575&f%5B%5D=694&f%5B%5D=693&f%5B%5D=691&f%5B%5D=689&f%5B%5D=576&f%5B%5D=688&f%5B%5D=687&f%5B%5D=685&f%5B%5D=683&f%5B%5D=577&f%5B%5D=682&f%5B%5D=681&f%5B%5D=678&f%5B%5D=675&f%5B%5D=578&f%5B%5D=674&f%5B%5D=673&f%5B%5D=671&f%5B%5D=669&f%5B%5D=579&f%5B%5D=668&f%5B%5D=667&f%5B%5D=666&f%5B%5D=664&f%5B%5D=663&f%5B%5D=665&f%5B%5D=662&f%5B%5D=660&f%5B%5D=580&f%5B%5D=659&f%5B%5D=658&f%5B%5D=657&f%5B%5D=656&f%5B%5D=581&f%5B%5D=655&f%5B%5D=654&f%5B%5D=653&f%5B%5D=652&f%5B%5D=651&f%5B%5D=650&f%5B%5D=649&f%5B%5D=648&f%5B%5D=582&f%5B%5D=647&f%5B%5D=646&f%5B%5D=645&f%5B%5D=644&f%5B%5D=643&f%5B%5D=642&f%5B%5D=583&f%5B%5D=641&f%5B%5D=640&f%5B%5D=634&f%5B%5D=628&f%5B%5D=584&f%5B%5D=627&f%5B%5D=626&f%5B%5D=622&f%5B%5D=617&f%5B%5D=585&f%5B%5D=616&f%5B%5D=615&f%5B%5D=614&f%5B%5D=613&f%5B%5D=612&f%5B%5D=611&f%5B%5D=610&f%5B%5D=586&f%5B%5D=609&f%5B%5D=608&f%5B%5D=606&f%5B%5D=604&f%5B%5D=603&f%5B%5D=602&f%5B%5D=601&f%5B%5D=600&f%5B%5D=587&f%5B%5D=599&f%5B%5D=598&f%5B%5D=597&f%5B%5D=596'
                            , 'games': '&f%5B%5D=34&f%5B%5D=59&f%5B%5D=58&f%5B%5D=57&f%5B%5D=56&f%5B%5D=55&f%5B%5D=54&f%5B%5D=53&f%5B%5D=902&f%5B%5D=35&f%5B%5D=36&f%5B%5D=65&f%5B%5D=64&f%5B%5D=63&f%5B%5D=62&f%5B%5D=37&f%5B%5D=38&f%5B%5D=69&f%5B%5D=68&f%5B%5D=67&f%5B%5D=66&f%5B%5D=39&f%5B%5D=74&f%5B%5D=73&f%5B%5D=72&f%5B%5D=71&f%5B%5D=70&f%5B%5D=40&f%5B%5D=78&f%5B%5D=77&f%5B%5D=76&f%5B%5D=75&f%5B%5D=41&f%5B%5D=43&f%5B%5D=81&f%5B%5D=44&f%5B%5D=45&f%5B%5D=91&f%5B%5D=90&f%5B%5D=89&f%5B%5D=88&f%5B%5D=87&f%5B%5D=86&f%5B%5D=85&f%5B%5D=84&f%5B%5D=83&f%5B%5D=82&f%5B%5D=571&f%5B%5D=46&f%5B%5D=100&f%5B%5D=99&f%5B%5D=98&f%5B%5D=97&f%5B%5D=96&f%5B%5D=95&f%5B%5D=101&f%5B%5D=102&f%5B%5D=103&f%5B%5D=104&f%5B%5D=105&f%5B%5D=106'
                           }
    name = 'UnionDHT'
    url = 'http://uniondht.org'
    MAX_PAGES_REQUEST = re.compile(r'<p style="float: left">.*? <b>\d</b> .*? <b>(\d+)</b></p>')
    SEARCH_TEMPLATE = 'http://uniondht.org/tracker.php?o=10&nm='
    AFTER_FINAL_PAGE = re.compile(r'<td class="row1 tCenter pad_8" colspan="12">.*?<\/td>')
    GET_TORRENT = re.compile(r'<p><a href="(.+?)" class="for_adblock">')
    GET_MAGNET = re.compile(r'href="(magnet:\?xt=urn:btih:.*announce)">?')


    # def __init__(self):
        # pass

    def download_torrent(self, info):
        logging.info('Starting download Torrent')
        torrent_page = get_page_data(info)
        # torrent_list = re.findall(self.GET_TORRENT, torrent_page)
        magnet_link = re.findall(self.GET_MAGNET, torrent_page)[0]
        print(magnet_link + " " + info)
        # torrent_link = str((torrent_list)[0])
        # a = get_page_data_encoded(torrent_link)
        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     temp_file.write(a)
        #     print(temp_file.name + ' ' + info)

    def search(self, what='ncis', cat='all'):
        logging.info('Beginning the search for {}'.format(what))
        ati_what = what.replace(' ', '+')
        page_offset = 0
        request_url = self.SEARCH_TEMPLATE + '&nm=' + str(ati_what) + '&start=' + str(page_offset) + self.supported_categories[cat.lower()]
        page_url = retrieve_url(request_url)
        total_pages = int(re.findall(self.MAX_PAGES_REQUEST, page_url)[0])
        while page_offset < (total_pages * 50):
            page_link = self.SEARCH_TEMPLATE + '&nm=' + str(ati_what) + '&start=' + str(page_offset) + self.supported_categories[cat.lower()]
            a = unionDHTParser(page_link)
            a.start()
            page_offset += 50
            logging.debug('Next query will start on page: {}'.format(page_offset))

        while (threading.active_count() > 1):
            pass

if __name__ == '__main__':
    logging.info('Running script directly')
    a = uniondht()
    # a.search('ncis', 'music')
    # a.download_torrent('http://uniondht.org/topic/41952-ncis-official-soundtrack.html')
    a.download_torrent('http://uniondht.org/topic/1551078-ncis-morskaya-politsiya-spetsotdel.html')
    
    pass
