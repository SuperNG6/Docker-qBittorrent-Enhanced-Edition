#VERSION: 1.0
#AUTHORS: gitDew

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import json
import random
import re
import string
import time

from helpers import retrieve_url
from novaprinter import prettyPrinter


class snowfl(object):
    url = "https://snowfl.com/"
    name = "snowfl"

    def search(self, what, cat='all'):
        token = self.fetch_token()
        query = self.generate_query(token, what)
        results = self.fetch_results(query)
        self.pretty_print_results(results)

    def fetch_token(self):
        file_name = "b.min.js"
        script = retrieve_url(self.url + file_name)

        # the token is a 37 char length string, hidden in the file we've fetched.
        # this is hacky, I know
        pattern = r'\b\w{37,37}\b'
        token = re.findall(pattern, script)[0]
        return token

    def generate_query(self, token, what):
        query = self.url + "/" + token + "/" + what + "/" + self.random_string(8) + "/0/SEED/NONE/1?_=" + str(
            int(time.time() * 1000))
        return query

    def random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def fetch_results(self, query):
        results = json.loads(retrieve_url(query))
        return results

    def pretty_print_results(self, results):
        for result in results:
            temp_result = {
                'name': result['title'],
                'size': result['size'],
                'seeds': result['seed'],
                'leech': result['leech'],
                'engine_url': self.url,
                'desc_link': result['pageLink']
            }
            try:
                temp_result['link'] = result['magnetLink']
            except KeyError:
                temp_result['link'] = str(-1)

            prettyPrinter(temp_result)
