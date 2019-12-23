#VERSION: 1.3
#AUTHORS: hoanns, nindogo
# movie and tv show site
# Will only parse the first search result site, sorry
# tv and movie category will not be differentiated

import re
import threading
# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url


# noinspection PyPep8Naming
class mkvcage(object):
    url = "https://www.mkvcage.ws"
    name = "MkvCage"
    supported_categories = {'all': True,
                            'movies': True,
                            'tv': True}
    games_to_parse = 10
    result_page_match = re.compile(r'<h2 class="entry-title"><a href="https:\/\/(.*?)"')    

    def handle_page(self, url):
        data = retrieve_url(url)
        size_match = re.compile(r'<strong>File\sSize:</strong>\s(.*?)(<br|\n)')
        try:
            size = size_match.findall(data)[0][0].replace('\r','')
        except IndexError:
            size = -1
        try:
            dl_match = re.compile(r'<title>(.+)<\/title>')
            dl = dl_match.findall(data)[0].replace('|','').replace('\r','')
        except IndexError:
            return
        try:
            magnet_match = re.compile(r'href="magnet:\?xt=urn:btih(.+)">MAGNET</a>',  re.I)
            ln = r'magnet:?xt=urn:btih' + magnet_match.findall(data)[0] + '&dn=' + dl
        except IndexError:
            ln_match = re.compile(r'href="\/torrents(.+)\.torrent"', re.I)
            ln = self.url + '/torrents' + ln_match.findall(data)[0] + '.torrent'
        result = {
            'name': dl,
            'size': size,
            'link': ln,
            'desc_link': url,
            'seeds': -1,
            'leech': -1,
            'engine_url': self.url
        }

        prettyPrinter(result)
        quit()

    def search(self, what, cat='all'):
        
        num_pages_match = re.compile(r'<li>…<\/li>\n<li><a href="https:\/\/www.mkvcage.ws\/page\/(\d+)')

        num_pages = 2
        page = 1
        while num_pages >= page:
            query = "https://www.mkvcage.ws/page/" + str(page) + "/?s=" + what
            data = retrieve_url(query)
            try:
                num_pages = int(num_pages_match.findall(data)[0])
            except IndexError:
                num_pages = page
            found_games = re.findall(self.result_page_match, data)

            if found_games:
                if self.games_to_parse > len(found_games):
                    self.games_to_parse = len(found_games)
                # handling each page in parallel, to not waste time on waiting for requests
                # for 8 entries this speeds up from 8s to 3s run time
                threads = []
                for i in range(self.games_to_parse):
                    # self.handle_page("http://" + found_games[i])
                    t = threading.Thread(target=self.handle_page, args=("https://" + found_games[i],))
                    threads.append(t)
                    t.start()

                # search method needs to stay alive until all threads are done
                # nindogo: not really, the threads don't need the primary thread
                # for t in threads:
                #     t.join()

            page += 1


if __name__ == "__main__":
    engine = mkvcage()
    engine.search('fire')
