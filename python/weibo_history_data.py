# -*- coding: utf-8 -*-

# create_date: '2018-07-05'

import datetime
import hashlib
import json
import time

import requests

# http://open.weibo.com/tools/console
access_token = '2.00Kmlw2DMf7ETBa6c71d8386txpVPB'
source       = '1345702386'

basic_url    = "https://c.api.weibo.com/2/search/statuses/historical/{}.json"


def create(start_date, end_date, keywords):
    """创建微博历史数据下载任务
    下载之前要新建查询任务，等到微博那边完成数据查询之后才能下载。

    检索任务可检索到2012年的数据，且每个任务的开始、结束时间区间最大不能超过一个月

    Args:
        start_date: 查询数据的开始时间戳
        end_date  : 查询数据的结束时间戳
        keywords  : 查询关键字，最多指定1000个关键词，每个关键词长度不超过24个中文字符或英文字符，由英文半角逗号分隔。

    Returns:
        task_id   : 查询任务的id
        secret_key: 任务密钥

    Exceptions:
        如果微博返回的数据是错误信息，则抛出异常。

    Links:
        http://open.weibo.com/wiki/C/2/search/statuses/historical/create
    """
    url = basic_url.format('create')

    with requests.Session() as s:
        data = {
            'starttime'   : start_date,
            'endtime'     : end_date,
            'q'           : keywords,
            'source'      : source,
            'access_token': access_token,
            'type'        : 0,
        }
        content = json.loads(s.post(url, data=data).content)
        if content.has_key('error_code'):
            raise AttributeError('{}: {}'.format(content['error_code'], content['error']))

        task_id    = content['task_id']
        secret_key = content['secret_key']

    return task_id, secret_key



def check(task_id, secret_key):
    """查看微博任务是否完成

    任务完成后才能进行下载

    Args:
        task_id   : 任务id
        secret_key: 任务密钥

    Returns:
        status: 如果完成，返回True，未完成返回False

    Exceptions:
        如果微博返回的数据是错误信息，则抛出异常。

    Links:
        http://open.weibo.com/wiki/C/2/search/statuses/historical/check
    """
    url = basic_url.format('check')
    with requests.Session() as s:
        timestamp = int(time.mktime(datetime.datetime.now().timetuple())*1000)
        signature = '{0}{1}{2}'.format(task_id, secret_key, timestamp)
        signature = hashlib.md5(signature).hexdigest()
        data = {
            'source'      : source,
            'access_token': access_token,
            'task_id'     : task_id,
            'timestamp'   : timestamp,
            'signature'   : signature,
            'type'        : 0,

        }
        content = s.get(url, params=data).content
        content = json.loads(content)
        if content.has_key('error_code'):
            raise AttributeError('{}: {}'.format(content['error_code'], content['error']))

        status = content['status']

    return status


def download(task_id, secret_key):
    """下载微博返回的结果

    将微博返回的结果保存到zip文件中。

    压缩包的解压密码为 task_id+secret_key

    Args:
        task_id   : 任务id
        secret_key: 任务密钥

    Links:
        http://open.weibo.com/wiki/C/2/search/statuses/historical/download
    """
    url = basic_url.format('download')
    with requests.Session() as s:
        timestamp = int(time.mktime(datetime.datetime.now().timetuple())*1000)
        signature = '{0}{1}{2}'.format(task_id, secret_key, timestamp)
        signature = hashlib.md5(signature).hexdigest()
        data = {
            'source'      : source,
            'access_token': access_token,
            'task_id'     : task_id,
            'timestamp'   : timestamp,
            'signature'   :signature,
        }
        content = s.get(url, params=data, stream=True)
        with open("{}.zip".format(task_id), 'wb') as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)

def main(start_date, end_date, keywords):
    # task_id, secret_key = create(start_date, end_date, keywords)
    task_id, secret_key = 132551495, u'6745322fa0dd7303507b' 
    print(task_id, secret_key)
    while(not check(task_id, secret_key)):
        print("job not finished, waiting...")
        time.sleep(5)
    download(task_id, secret_key)


if __name__ == '__main__':
    start_date = int(time.mktime(datetime.datetime(2017, 11, 5).timetuple())*1000)
    end_date   = int(time.mktime(datetime.datetime(2017, 11, 6).timetuple())*1000)
    main(start_date, end_date, '英雄联盟全球总决赛')
