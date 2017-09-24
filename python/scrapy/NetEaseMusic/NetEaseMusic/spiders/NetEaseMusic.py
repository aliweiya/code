# -*- coding: utf-8 -*-

import sys

from scrapy.http import Request
from scrapy import Spider
from bs4 import BeautifulSoup

sys.path.append('/../')

from NetEaseMusicModel import save_singer


class NetEaseMusic(Spider):
    name = 'NetEaseMusic'

    # enter from singers
    singer_category = [
        1001, 1002, 1003, # Chinese
        2001, 2002, 2003, # Europe and America
        6001, 6002, 6003, # Japanese
        7001, 7002, 7003, # Korea
        4001, 4002, 4003  # Other
        ]

    alphabet_list = [i for i in range(65, 91)]
    alphabet_list.extend([0])

    singer_url = 'http://music.163.com/discover/artist/cat?id=%d&initial=%d'

    def start_requests(self):
        for category in self.singer_category:
            for alphabet in self.alphabet_list:
                url = self.singer_url % (category, alphabet)
                meta = {'category': category, 'alphabet': alphabet}
                yield Request(url, callback=self.parse_singer, meta=meta)

    def parse_singer(self, response):
        category = response.meta['category']
        alphabet = response.meta['alphabet']

        # with open('%d_%d.html' % (category, alphabet), 'w') as f:
        #     f.write(response.body)
        #     f.close()

        soup = BeautifulSoup(response.body)
        singer_list = soup.find('ul', id='m-artist-box')
        singer_li = singer_list.find_all('li')
        for li in singer_li:
            li_class = li.get('class')
            if (not li_class) or li_class == 'line':
                link = li.p.a

            elif li.get('class') == 'sml':
                link = li.a

            singer_id = link.get('href').replace('/artist?id=', '')
            singer_name = link.text

            save_singer()

            