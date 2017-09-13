# -*- coding: utf-8 -*-
import csv
from pymongo import MongoClient
import datetime
import codecs


client = MongoClient('mongodb://ugc:a1b2c3d4@10.0.0.110:29019/crawler')
# client = MongoClient('10.0.0.110', 29019)
# db = client['crawler']
# db.authenticate('ugc', 'a1b2c3d4')

print 'connection established!'
db = client['crawler']

start_time = datetime.datetime.strptime("2016-08-01 00:00:00","%Y-%m-%d %H:%M:%S")
end_time = datetime.datetime.strptime("2017-07-31 00:00:00","%Y-%m-%d %H:%M:%S")

def export_volkswagen_data():

    csvFile = file('volkswagen.csv', 'wb')
    csvFile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvFile)

    header = ['品牌', '车系', '查看量', '回复量', '维度', '子维度']
    writer.writerow(header)

    for r in db.main_label_filter.find({"brand": "大众", "status": 3, "pp_date":{"$gt":start_time, "$lt":end_time}}).batch_size(1000):

        print 'get', r['pp_id']

        r_list = []
        r_list.append(r['brand'].encode('utf-8'))
        r_list.append(r['series'].encode('utf-8'))

        pp = db.public_praise.find_one({"_id":r['pp_id']})
        r_list.append(str(pp['k_views']))
        r_list.append(str(pp['k_comments']))

        if r['tree'].encode('utf-8') == "QVOC_TID":
        #  if r['label'].encode('utf-8')[-1] in ["褒", "贬"]:
            r_list.append(r['label'].encode('utf-8'))
            
        else:
            label_list = r['label'].encode('utf-8').split('/')
            label_first = "/".join(label_list[:-1])
            label_second = label_list[-1]
            r_list.append(label_first)
            r_list.append(label_second)

        print ','.join(r_list)
        writer.writerow(r_list)

    csvFile.close()

def export_other_data():

    csvFile = file('other.csv', 'wb')
    csvFile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvFile)

    header = ['品牌', '车系', '查看量', '回复量', '维度', '子维度']
    writer.writerow(header)

    i = 0
    for r in db.main_label_filter.find({"brand": {"$ne": "大众"}, "pp_date": {"$gt":start_time, "$lt":end_time}}).batch_size(1000):

        print 'get', r['pp_id']
        print i
        i += 1

        r_list = []
        r_list.append(r['brand'].encode('utf-8'))
        r_list.append(r['series'].encode('utf-8'))

        pp = db.public_praise.find_one({"_id":r['pp_id']})
        r_list.append(str(pp['k_views']))
        r_list.append(str(pp['k_comments']))

        if r['tree'].encode('utf-8') == "QVOC_TID":
        # if r['label'].encode('utf-8')[-1] in ["褒", "贬"]:
            r_list.append(r['label'].encode('utf-8'))

        else:
            label_list = r['label'].encode('utf-8').split('/')
            label_first = "/".join(label_list[:-1])
            label_second = label_list[-1]
            r_list.append(label_first)
            r_list.append(label_second)

        print ','.join(r_list)
        writer.writerow(r_list)

    csvFile.close()
        
if __name__ == '__main__':
    # export_volkswagen_data()
    export_other_data()
