# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy import Spider
from bs4 import BeautifulSoup


class Album(Spider):
    name = 'Album'

    client = MongoClient('localhost', 27017)
    db = client['NetEaseMusic']

    album_url = 'http://music.163.com/artist/album?id=%d&limit=200'

    def start_requests(self):
