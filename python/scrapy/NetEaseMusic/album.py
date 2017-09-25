import os

from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['NetEaseMusic']

def id_and_name():
    for parent, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            print filename
            with open(filename) as f:
                try:
                    soup = BeautifulSoup(''.join(f.readlines()))
                    album_list = soup.find('ul', id='m-song-module')
                    album_li = album_list.find_all('li')
                    for li in album_li:
                        link = li.p.a
                        albumId = link.get('href').replace('/album?id=', '')
                        albumName = link.text

                        if db.album.find({'id':albumId}).count() == 0:
                            album = {'id': albumId, 'name': albumName}
                            print 'insert %s succeeded!' %(albumId)
                            db.album.save(album)

                except Exception, e:
                    print 'occuring an error when parsing page %s' %(filename)
                    print e

                f.close()

if __name__ == '__main__':
    id_and_name()
    print 'done'