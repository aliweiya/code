# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy import Spider
from bs4 import BeautifulSoup
from pymongo import MongoClient


class Album(Spider):
    name = 'Album'

    client = MongoClient('localhost', 27017)
    db = client['NetEaseMusic']

    album_url = 'http://music.163.com/artist/album?id=%s&limit=200'

    def start_requests(self):
        for singer in self.db.singer.find():
            singerId = singer['id']
            url = self.album_url % (singerId)
            print url
            meta = {'singerId': singerId}
            yield Request(url, callback=self.parse_album, meta=meta)

    def parse_album(self, response):
        singerId = response.meta['singerId']
        # filename = './album/%s.html'%(singerId)
        # filename = filename.replace(' ', '')
        # with open(filename, 'w') as f:
        #     f.write(response.body)
        #     f.close()

        try:
            soup = BeautifulSoup(response.body)
            album_list = soup.find('ul', id='m-song-module')
            album_li = album_list.find_all('li')
            for li in album_li:
                link = li.p.a
                albumId = link.get('href').replace('/album?id=', '')
                albumName = link.text

                if self.db.album.find({'id':albumId}).count() == 0:
                    album = {'id': albumId, 'name': albumName}
                    self.db.album.save(album)
                    print 'insert %s succeeded!' %(albumId)

        except Exception, e:
            print e

