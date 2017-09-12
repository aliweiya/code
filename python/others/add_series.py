from pymongo import MongoClient


client = MongoClient('mongodb://dds-bp1dfb31d5fbb4741.mongodb.rds.aliyuncs.com:3717/')
db = client['crawler']
db.authenticate('ugc', 'a1b2c3d4')

def add_series():
    for keyword in db.subscribe_keywords_ugc.find({}).batch_size(1000):
        print keyword['keyword']
        keyword['group'] = keyword['BrandName'] if keyword.has_key('BrandName') else '(None)'
        car_series = db.car_series.find({'name': {'$regex':keyword['keyword'].upper()}})
        for car in car_series:
            keyword['BrandName'] = car['brandName']
            keyword['SeriesName'] = car['name']
            keyword['SeriesId'] = car['autohome_id']
            keyword['group'] = keyword['BrandName']
            print keyword
            break
        db.subscribe_keywords_ugc.save(keyword)

if __name__ == '__main__':
    add_series()
    print db.subscribe_keywords_ugc.find({'BrandName':{'$exists':False}}).count()