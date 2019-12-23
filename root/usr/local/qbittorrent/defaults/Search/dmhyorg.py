
#VERSION: 1.00
#AUTHORS: xyau (xyauhideto@gmail.com)

# MIT License
#
# Copyright (c) 2018 xyau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the right
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software i
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# qBT
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter

# parser
from re import compile as re_compile

class dmhyorg(object):
    url = "https://share.dmhy.org"
    name = "DMHY"
    supported_categories = {"all":0,"anime":2,"pictures":3,"music":4,"tv":6,"games":9}

    def download_torrent(self, info):
        """ Downloader """
        print(download_file(info))

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat="all"):
        """ Performs search """

        def get_data(url):
            highlight = re_compile('<span class="keyword">([^<]+)</span>')
            get_next = re_compile('(?s)"fl".+href="([^"]+)">下一')
            get_item = re_compile('(?m)<a href="(/topics/view/[^"]+)"[^>]+>\s*([^<]*)</a>(?:\s*.*){2}(magnet:[^"]+)".*\s*.*>([\d\.]+)(\w+)</td[^/]+btl_1">([\d-]+)</span></td>\s*[^/]+bts_1">([\d-]+)<')
            html = retrieve_url(url)
            next_page = get_next.search(html)
            # clear highlighting
            return [get_item.findall(highlight.sub(r"\1",html)),
                    next_page and self.url + next_page.group(1)]

        query = "%s/topics/list/?keyword=%s&sort_id=%d" % (
            self.url, what, self.supported_categories.get(cat, "0"))

        while query:
            [data,query] = get_data(query)
            for item in data:
                prettyPrinter({
                    "desc_link":self.url+item[0],
                    "name":item[1],
                    "link":item[2],
                    "size":str(int(float(item[3]) * 2 ** (10 * (1 + 'kmgtpezy'.find(item[4][0].lower()))))),
                    "seeds":0 if "-" == item[5] else int(item[5]),
                    "leech":0 if "-" == item[6] else int(item[6]),
                    "engine_url":self.url
                })

if __name__ == "__main__":
    engine = dmhyorg()
    engine.search('conan')
