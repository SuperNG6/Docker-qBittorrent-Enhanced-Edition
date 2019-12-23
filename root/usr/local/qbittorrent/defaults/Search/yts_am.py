# VERSION: 1.0
# AUTHORS: mauricci

from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
import json, math

try:
    # python3
    from html.parser import HTMLParser
except ImportError:
    # python2
    from HTMLParser import HTMLParser


class yts_am(object):
    url = 'https://yts.am/'
    name = 'Yts.am'
    # category not used, just declared for qbt
    supported_categories = {'all': '', 'movies': ''}

    def search(self, what, cat='all'):
        page = 1#current page number
        limit = 20  # results per page
        moviesPages = 10  # actual total number of pages

        while page <= 10 and page <= moviesPages:  # max 10 pages
            url = self.url + 'api/v2/list_movies.json?query_term={0}&page={1}&limit={2}'.format(what, page, limit)
            page += 1
            html = retrieve_url(url)
            jsonData = json.loads(html)
            self.processJson(jsonData)
            moviesPages = math.ceil(float(jsonData['data']['movie_count']) / limit)

    def getSingleData(self):
        return {'name': '-1', 'seeds': '-1', 'leech': '-1', 'size': '-1', 'link': '-1', 'desc_link': '-1',
                'engine_url': self.url}

    def processJson(self, json):
        movieData = self.getSingleData()
        for movie in json['data']['movies']:
            movieData['name'] = '{} - {}'.format(movie['title'], movies['year'])
            movieData['desc_link'] = movie['url']
            for torrent in movie['torrents']:
                movieData['seeds'] = torrent['seeds']
                movieData['leech'] = torrent['peers']
                movieData['size'] = torrent['size']
                movieData['link'] = torrent['url']
                prettyPrinter(movieData)

    def download_torrent(self, info):
        """ Downloader """
        print(download_file(info))


# script test
if __name__ == "__main__":
    y = yts_am()
    y.search('tomb%20raider')
