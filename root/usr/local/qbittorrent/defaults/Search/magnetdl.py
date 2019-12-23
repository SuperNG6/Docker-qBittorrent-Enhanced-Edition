#VERSION: 1.3
#AUTHORS: hoanns,nindogo
# magnetdl.com
# first thirty pages

import re
# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url


# noinspection PyPep8Naming
class magnetdl(object):
    url = "http://www.magnetdl.com/"
    name = "MagnetDL"
    result_page_match = re.compile(
        '<td\sclass="m"><a\shref="(magnet.*?)"\stitle=".*?class="n"><a\shref="(.*?)"\stitle="(.*?)">.*?<td\sclass="t.">.*?</td><td>.*?</td><td>(.*?)</td><td\sclass="s">(.*?)</td><td\sclass="l">(.*?)</td>')
    total_results_num = re.compile(
        r'<div id="footer">Found <strong>(.*)<\/strong> Magnet Links for <i>')

    def search(self, what, cat='all'):
        what = what.lower()
        running_total, total_results, pages = 0, 1, 0

        while running_total < total_results and pages <= 29:
            pages += 1
            query = self.url + what[:1] + '/' + what +'/' + str(pages)
            # print(query)
            data = retrieve_url(query)
            total_results = int(re.findall(self.total_results_num, data)[0].replace(',', ''))
            results = re.findall(self.result_page_match, data)

            for result in results:
                temp_result = {
                    'name': result[2].replace('|', '') ,
                    'size': result[3].replace(',', '') ,
                    'link': result[0],
                    'desc_link': self.url[:-1] + result[1],
                    'seeds': result[4],
                    'leech': result[5],
                    'engine_url': self.url
                }
                prettyPrinter(temp_result)
                running_total += 1

        return


if __name__ == "__main__":
    engine = magnetdl()
    engine.search('Ebook')
