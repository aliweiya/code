# —*— coding:utf-8 -*-

import sys
import logging
import datetime
import time
import traceback
import json
from bs4 import BeautifulSoup
import requests
import random
import struct
import socket
import base64
import os
import re
from collections import defaultdict

from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

import commands
from fontTools.ttLib import TTFont

sys.path.append("./../../../")

from commonScripts.LoggerManager import LoggerManager
from commonScripts.get_proxy_ip import ProxyIp, get_proxy_ip_list, ipObjectsToList
from commonScripts.proxy_settings import *
from commonScripts.tong_list import series_list
from commonScripts.commonFunction import *
from parseScripts.autohome import autohomeKAnalysis
from crawlerMongodb.model import *

reload(sys)
sys.setdefaultencoding('utf-8')

executor = ThreadPoolExecutor(10)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['social_survey']

pp_page_first = "https://k.autohome.com.cn/%s/ge0/0-0-2/"
pp_page_next = "https://k.autohome.com.cn/%s/ge0/0-0-2/index_%s.html"

usa = [
 "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
 "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
]

RANDOM_IP_POOL=['192.168.10.222/0']

word = ['一', '七', '三', '上', '下', '不', '中', '档', '比', '油',
        '泥', '灯', '九', '了', '二', '五', '低', '保', '光', '八',
        '公', '六', '养', '内', '冷', '副', '加', '动', '十', '电',
        '的', '皮', '盘', '真', '着', '路', '身', '软', '过', '近',
        '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢',
        '味', '和', '响', '四', '地', '坏', '坐', '外', '多', '大',
        '好', '孩', '实', '小', '少', '短', '矮', '硬', '空', '级',
        '耗', '雨', '音', '高', '左', '开', '当', '很', '得', '性',
        '自', '手', '排', '控', '无', '是', '更', '有', '机', '来',
        ]


def __get_random_ip():
    str_ip = RANDOM_IP_POOL[random.randint(0,len(RANDOM_IP_POOL) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I',socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | ( 1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))

headers = {
    'X-Forwarded-For': __get_random_ip(),
}


def get_proxy_ip_list(index=1):
    if len(PROXY_URL_LIST) >0 :
        proxy_logger.debug('代理ip充足，进行使用')
        return PROXY_URL_LIST
    response  = requests.get(url = PROXY_URL)
    for i in range(1,PROXY_RETRY_TIMES):
        try:
            json_ip = requests.get(PROXY_URL).text
            response = json.loads(json_ip)
            proxy_logger.debug('代理返回的txt为:%s' %(json_ip))
            if response['ERRORCODE'] !="0":
                proxy_logger.debug('代理ip请求太频繁,开始重新请求,第%d次请求' %(i))
                if i%100 == 0:
                    proxy_logger.debug('!!!请求太频繁，开始进行time sleep 10s再重新请求')
                continue
            user_pass = '132939803024:123456'
            for ip in json.loads(json_ip)['RESULT']:
                kwargs = {}
                ip_url = IP_URL_BASE %(ip['ip'],str(ip['port']))
                kwargs['ip'] = ip_url
                ip_obj = ProxyIp(**kwargs)
                ip_obj.save()
                kwargs['source'] = 'default'
                kwargs['crawl_date'] = datetime.datetime.now()+datetime.timedelta(hours=-8)
                db.proxy_ip.insert_one(kwargs)
                db.proxy_ip_gr.insert_one(kwargs)
                db.proxy_ip_ljh.insert_one(kwargs)
            return PROXY_URL_LIST
        except Exception as e:
            return PROXY_URL_LIST
            proxy_logger.error('请求代理url失败，请检查网络或者订单信息')


def remove_unuseful_proxy_ip(proxy_ip):
    try:
        ProxyIp.removeIp(proxy_ip)
    except Exception, e:
       logging.error(e)
    check_ip_list()


def check_ip_list(PROXY_URL_LIST=[]):
    if ProxyIp.getIpCount() == 0:
        proxy_logger.debug('代理池已空，现在开始补充代理ip')
        get_proxy_ip_list()    


def get_reponse(url=None, times=0):
    check_ip_list()
    global SUCCESS_PAGES, REPARIED_PAGES
    proxy = random.choice(ipObjectsToList())
    proxies = {'https': proxy}
    if 'userverify/index?' in url:
       url ='https://'+ url.split('//')[1]
       proxy_logger.error('注意注意。url有极大异常:%s' %(url))
    try:
        headers= {}
        headers['X-Forwarded-For'] =  __get_random_ip()

        headers["User-Agent"]= random.choice(usa)
        user_pass = '132939803024:123456'

        encoded_user_pass = base64.b64encode(user_pass)
        headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        response  = requests.get(url=url, proxies=proxies, timeout=REQUEST_TIME_OUT, headers=headers, verify=False)
    except Exception as e:
        proxy_logger.error('代理ip:%s被限制，现开始切换，url为:%s，错误信息为：%s' %(proxies, url, traceback.format_exc()))
        remove_unuseful_proxy_ip(proxy)
        response = get_reponse(url)
        REPARIED_PAGES += 1   
        return response
    if response.status_code in BASE_CODE and 'userverify/index?' not in response.url:
        SUCCESS_PAGES += 1       
        if response.elapsed.seconds > MIN_RESPONSE_SECONDS:
            proxy_logger.debug('该代理ip属于次品，花了%d获取网页，开始切换' %(response.elapsed.seconds))
            remove_unuseful_proxy_ip(proxy)
    else:
        proxy_logger.error('!!!抓取异常,url:%s,状态码为%s' %(response.url, response.status_code))
        remove_unuseful_proxy_ip(proxy)
        proxy_logger.debug('开始第%d次补爬数据，url为:%s,header XFF:%s, ua:%s' %(times, url,headers['X-Forwarded-For'], headers["User-Agent"]))
        while times<RESPONSE_TIMES:
            times+=1
            response = get_reponse(url, times)
            REPARIED_PAGES += 1
            if response.status_code in BASE_CODE and 'userverify/index?' not in response.url:
                proxy_logger.error('补爬url:成功 %s' %(url))
                return response
        proxy_logger.error('!!!重试第%d次依然失败，请检查具体情况' %(RESPONSE_TIMES)) 
    return response 


def get_complete_text_autohome(text):
    for item in re.findall(ur'<!--athm-->[\w\W]+?<!--@athm_js@-->', text):
        index = text.index(item)
        chinese = re.search(ur'[\u4e00-\u9fa5]+', text[index+len(item):]) 
        if chinese is not None:
            chinese = chinese.group()

        chinese_index = re.search(ur'\d[\d|;]+[\d]', text[index+len(item):])
        if chinese_index is not None:
            chinese_index = chinese_index.group()
        chinese_indexes = chinese_index.split(';')
        try:
            chinese = [chinese[int(i)] for i in chinese_indexes]
        except Exception, e:
            # 只有一个被替换的字
            pass    
        spans = re.findall(ur'<span[\w\W]+?</span>', item)
        for span in spans:
            span_index = span.split('_')[1][2:]
            word = chinese[int(span_index)]
            item = text.replace(span, word)
    return text


def parse():
    pool = Pool(5)
    for serie in series_list('autohome'):
        serie_id = serie['series_id'].replace('autohome_', '')
        pool.map(parse_serie, [serie_id])
        # parse_serie(serie_id)

    pool.join()
    pool.close()


def parse_serie(serie_id):
    url = pp_page_first % (serie_id)
    parse_logger.info('start crawling page %s' % (url))
    response = get_reponse(url)
    response.encoding = 'gbk'
    parse_logger.error('Crawled %s' % (response.url))
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='gbk')
    detail_divs = soup.find_all('div', 'title-name name-width-01')
    parse_logger.error('the number of divs in url %s is:%d' %(url, len(detail_divs)))
    for detail_div in detail_divs:
        detail_url = 'https:' + detail_div.find('a').attrs['href']
        detail_time = detail_div.find('a').text
        detail_time = datetime.datetime.strptime(detail_time, '%Y-%m-%d')
        parse_logger.info('口碑发布时间为%s' %(detail_time))
        time_now = datetime.datetime.now()
        parse_logger.info('现在时间为%s' %(time_now))

        executor.submit(parse_detail_page, detail_url)


def parse_detail_page(detail_url):
    parse_logger.info('start crawling page %s' % (detail_url))
    response = get_reponse(detail_url)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='gbk')
    ret = {"k_source":"autohome"}
    ret['k_type'] = PublicPraise.K_TYPE_ENUM.PRAISE
    ret["k_title"] = soup.title.string
    ret["k_url"] = detail_url
    parse_logger.info('k_title is %s, k_url is %s' % (ret["k_title"], ret["k_url"]))
    row = soup.find("div","row")
    
    if row == None:
        raise ValueError("the html_doc has no valid data: %s" % (fn))
    user = row.find("dl","user-cont")
    if user == None:
        raise ValueError("the html_doc has no valid user: %s" % (fn))
    usernameDiv = user.find("div","user-name")
    if usernameDiv == None:
        raise ValueError("the html_doc has no valid user-name: %s" % (fn))
    usernames = usernameDiv.find_all("a")

    ret['k_content'] = soup.find('div', 'text-con').text

    if 'span' in ret['k_content']:
        raise ValueError('还有未替换的标签') 

    ret["user_name"] = usernames[0].text.strip()
    ret["user_url"] = usernames[0].get("href")
    userlevelDiv = usernameDiv.find("div", "rank")
    if userlevelDiv!=None:
        ret["user_level"] = int(userlevelDiv.find("i").get_text().replace('LV','').strip())
    userinfoDiv = user.find("div","user-info")

    user_type = userinfoDiv.find("i")
    if user_type != None:
        ret["user_type"] = u'认证用户'
    else:
        ret["user_type"] = u'未认证用户'

    time_a=row.find_all("div","cont-title")
    time_b = time_a[len(time_a)-1].find('b')
    ret["k_date"] = parser.parse(time_b.text.strip().replace(u'年','-').replace(u'月','-').replace(u'日',''))
    try:
        ret["k_level"] = K_LEVEL_MAP.get(row.find("div","nav-sub").i.get("class")[0],"unknown")
    except Exception, e:
        ret["k_level"] = 'unknown'

    chooses = row.find_all("dl")

    choosesMap = {}
    for choose in chooses:
        key = choose.dt.text.strip()
        value = choose.dd.text.strip()
        choosesMap[key] = value
    ret["k_c_set"]        = choosesMap.get(CN_C_TYPE      ,'').split('\n')[0]
    ret["k_c_type"]       = choosesMap.get(CN_C_TYPE      ,'').split('\n')[-1]
    ret['k_c_agency'] = choosesMap.get(CN_C_AGENCY, '').replace('&nbsp','')
    ret["k_c_bare_price"] = choosesMap.get(CN_C_BARE_PRICE,'')
    ret["k_c_buy_date"]   = choosesMap.get(CN_C_BUY_DATE  ,'')
    m = re.match("(\d{4}).*?(\d{1,2}).*",ret["k_c_buy_date"])
    if m:
        ret["k_c_buy_year"]  = int(m.group(1))
        ret["k_c_buy_month"] = int(m.group(2))
    ret["k_c_buy_addr"]   = choosesMap.get(CN_C_BUY_ADDR  ,'')
    ret["k_c_buy_aim"]    = choosesMap.get(CN_C_BUY_AIM   ,'').split('\n')
    ret["k_c_oil_wear"]   = choosesMap.get(CN_C_OIL_WEAR  ,'').split('\n')[0]
    ret["k_c_mileage"]    = choosesMap.get(CN_C_OIL_WEAR  ,'').split('\n')[-1]
    ret["k_c_fen_kj"]     = int(choosesMap.get(CN_C_FEN_KJ    ,0))
    ret["k_c_fen_dl"]     = int(choosesMap.get(CN_C_FEN_DL    ,0))
    ret["k_c_fen_ck"]     = int(choosesMap.get(CN_C_FEN_CK    ,0))
    ret["k_c_fen_yh"]     = int(choosesMap.get(CN_C_FEN_YH    ,0))
    ret["k_c_fen_ss"]     = int(choosesMap.get(CN_C_FEN_SS    ,0))
    ret["k_c_fen_wg"]     = int(choosesMap.get(CN_C_FEN_WG    ,0))
    ret["k_c_fen_ns"]     = int(choosesMap.get(CN_C_FEN_NS    ,0))
    ret["k_c_fen_xj"]     = int(choosesMap.get(CN_C_FEN_XJ    ,0))
    ret["k_c_imglist"]    = []

    imglist = row.find("ul","img-list")
    if imglist is not None:
        for li in imglist.find_all('li'):
            ret["k_c_imglist"].append(li.get("souce"))
    try:
        fn = row.find("div","inform")
        ret["k_views"]    = int(fn.find("div","fn-left").a.text)
        ret["k_supports"] = int(fn.find("div","fn-right").find("label","supportNumber").text)
        ret["k_comments"] = int(fn.find("div","fn-right").find("label","CommentNumber").text)
    except Exception, e:
        pass

    fillExtraInfoForPublicPraise(ret)
    ret['crawl_date']=datetime.datetime.now()
    pp = PublicPraise(**ret)
    pp.save()
    parse_logger.info('pp_id here!%s'%(pp.k_id))


# class LogClass(object):
#     def __new__(cls, *args, **kw):
#         if not hasattr(cls, '_instance'):
#             orig = super(LogClass, cls)
#             cls._instance = orig.__new__(cls, *args, **kw)
#             cls.logger = logging.getLogger(cls.__name__)
#             cls.logger.debug("%s init success!!! " %(cls.__name__))
#         return cls._instance


if __name__ == '__main__':
    # LoggerManager.initlogging(loglevel=logging.INFO, needConsle=True)
    # logger = LogClass().logger
    logging.basicConfig(filemode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    parse_handler = logging.FileHandler('/home/mas/log/spider_log/praise/daily_autohome_parse.log', mode='w')
    parse_handler.setFormatter(formatter)
    parse_logger = logging.getLogger('parse_logger')
    parse_logger.addHandler(parse_handler)

    proxy_handler = logging.FileHandler('/home/mas/log/spider_log/proxy.log', mode='w')
    proxy_handler.setFormatter(formatter)
    proxy_logger = logging.getLogger('proxy_logger')
    proxy_logger.addHandler(proxy_handler)

    parse()
