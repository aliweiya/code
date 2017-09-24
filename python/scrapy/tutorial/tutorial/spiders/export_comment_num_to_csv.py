# -*- coding: utf-8 -*-

import csv
from pymongo import MongoClient
import codecs


def export_to_csv():

    client = MongoClient('127.0.0.1', 27017)
    db = client['music']

    csvFile = file('comments.csv', 'wb')
    csvFile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvFile)

    for r in db.comment.find({'total': {'$gt': 20000}}).sort('total').batch_size(1000):
        r_list = []
        r_list.append(r['m_name'].encode('utf-8'))
        r_list.append(r['total'])
        print r_list

        writer.writerow(r_list)

    csvFile.close()

if __name__ == '__main__':
    export_to_csv()