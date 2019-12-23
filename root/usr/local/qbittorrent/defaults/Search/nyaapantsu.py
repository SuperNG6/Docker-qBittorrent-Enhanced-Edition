# -*- coding: utf-8 -*-
#VERSION: 1.2
#AUTHORS: Joost Bremmer (toost.b@gmail.com)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


from enum import Enum
try:
    from HTMLParser import HTMLParser

except ImportError:
    from html.parser import HTMLParser

# import qBT modules
try:
    from novaprinter import prettyPrinter
    from helpers import retrieve_url
except:
    pass


class nyaapantsu(object):
    """Class used by qBittorrent to search for torrents"""

    url = 'https://nyaa.pantsu.cat'
    name = 'Nyaa.pantsu'
    # defines which search categories are supported by this search engine
    # and their corresponding id. Possible categories are:
    # 'all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures',
    # 'books'
    supported_categories = {
            'all': '_',
            'anime': '3_',
            'books': '4_',
            'music': '2_',
            'pictures': '6_',
            'software': '1_',
            'tv': '5_',
            'movies': '5_'}

    class NyaaPantsuParser(HTMLParser):
        """ Parses Nyaa.pantsu browse page for search resand prints them"""

        class DataType(Enum):
            """Enumeration to keep track of the TD Type to use in handle_data()'"""
            NONE = 0
            NAME = 1
            SEEDS = 2
            LEECH = 3
            SIZE = 4


        def __init__(self, res=(), url="https://nyaa.pantsu.cat"):
            try:
                super().__init__()
            except:
                #  See: http://stackoverflow.com/questions/9698614/
                HTMLParser.__init__(self)

            self.engine_url = url
            self.results = res
            self.curr = None
            self.td_type = self.DataType.NONE

        def handle_starttag(self, tag, attr):
            """Calls element specific functions based on tag."""
            if tag == 'a':
                self.start_a(attr)
            if tag == 'tr':
                self.start_tr(attr)
            if tag == 'td':
                self.start_td(attr)

        def start_tr(self, attr):
            params = dict(attr)
            if 'class' in params and params['class'].startswith('torrent-info'):
                self.curr = {'engine_url': self.engine_url}

        def start_a(self, attr):
            params = dict(attr)
            # get torrent name
            if 'href' in params and params['href'].startswith('/view/'):
                if self.curr:
                    self.curr['desc_link'] = self.engine_url + params['href']
                # also get name from handle_data()
                self.td_type = self.DataType.NAME
            # get torrent magnet link
            elif 'href' in params and params['href'].startswith("magnet:?"):
                if self.curr:
                    self.curr['link'] = params['href']

        def start_td(self, attr):
            """Parses TD elements and sets self.td_type based on its html class.

            If last TD element for the current hit is reached it appends it to
            results and cleans up.
            """
            params = dict(attr)

            # get seeds from handle_data()
            if 'class' in params and params['class'].startswith("tr-se"):
                self.td_type = self.DataType.SEEDS
            # get leechers from handle_data()
            elif 'class' in params and params['class'].startswith("tr-le"):
                self.td_type = self.DataType.LEECH
            # get size from handle_data()
            elif 'class' in params and params['class'].startswith("tr-size"):
                self.td_type = self.DataType.SIZE
            # we've reached the end of this result; save it and clean up.
            elif 'class' in params and params['class'].startswith("tr-date"):
                self.results.append(self.curr)
                self.td_type = self.DataType.NONE
                self.curr = None
            # default: current innerContent does not concern us: pass.
            else:
                self.td_type = self.DataType.NONE

        def handle_data(self, data):
            """Strip textContent data for search result based on td type"""
            # Get result name
            if self.td_type == self.DataType.NAME:
                if 'name' not in self.curr:
                    self.curr['name'] = ''
                self.curr['name'] += data.strip()
                self.td_type = self.DataType.NONE
            # Get no. of seeds
            elif self.td_type == self.DataType.SEEDS:
                try:
                    self.curr['seeds'] = int(data.strip())
                except:
                    self.curr['seeds'] = -1
                finally:
                    self.td_type = self.DataType.NONE
            # Get no. of leechers
            elif self.td_type == self.DataType.LEECH:
                try:
                    self.curr['leech'] = int(data.strip())
                except:
                    self.curr['leech'] = -1
                finally:
                    self.td_type = self.DataType.NONE
            # Get size
            elif self.td_type == self.DataType.SIZE:
                size = data.strip()
                self.curr['size'] = data.strip()
                self.td_type = self.DataType.NONE
            # Default: self.td_type is unset, current textConent is not
            # interesting, do nothing.
            else:
                pass

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        """
        Retreive and parse engine search results by category and query.

        Parameters:
        :param what: a string with the search tokens, already escaped
                     (e.g. "Ubuntu+Linux")
        :param cat:  the name of a search category, see supported_categories.
        """

        page = 1
        hits = []
        parser = self.NyaaPantsuParser(hits, self.url)
        while True:
            url = str(
                    "{0}/search/{1}?s=0&sort=5&order=false&max=300&c={2}&q={3}"
                    .format(self.url,
                            page,
                            self.supported_categories.get(cat),
                            what))
            # pantsu is very volatile.
            try:
                res = retrieve_url(url)
                parser.feed(res)
            except:
                pass

            for each in hits:
                prettyPrinter(each)

            if len(hits) < 300:
                break
            del hits[:]
            page += 1

        parser.close()
