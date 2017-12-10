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


def get_char(js, replace_count):
    all_var = {}
    # 判断混淆 无参数 返回常量 函数
    if_else_no_args_return_constant_function_functions = []
    """
    function zX_() {
            function _z() {
                return '09';
            };
            if (_z() == '09,') {
                return 'zX_';
            } else {
                return _z();
            }
        }
    """
    constant_function_regex4 = re.compile("""
        function\s+\w+\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*else\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*
        \}
        """,
            re.X)
    l = constant_function_regex4.findall(js)
    for i in l:
        function_name = re.search("""
        function\s+(\w+)\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*else\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*
        \}
        """, i,
            re.X)
        if_else_no_args_return_constant_function_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b,c,d = function_name.groups()
        all_var["%s()"%a] = d if b == c else b


    # 判断混淆 无参数 返回函数 常量
    if_else_no_args_return_function_constant_functions = []
    """
    function wu_() {
            function _w() {
                return 'wu_';
            };
            if (_w() == 'wu__') {
                return _w();
            } else {
                return '5%';
            }
        }
    """
    constant_function_regex5 = re.compile("""
        function\s+\w+\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*else\s*\{\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*
        \}
        """,
            re.X)
    l = constant_function_regex5.findall(js)
    for i in l:
        function_name = re.search("""
        function\s+(\w+)\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*else\s*\{\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*
        \}
        """, i,
            re.X)
        if_else_no_args_return_function_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b,c,d = function_name.groups()
        all_var["%s()"%a] = b if b == c else d


    # var 参数等于返回值函数
    var_args_equal_value_functions = []
    """
    var ZA_ = function(ZA__) {
            'return ZA_';
            return ZA__;
        };
    """
    constant_function_regex1 = re.compile("var\s+[^=]+=\s*function\(\w+\)\{\s*[\'\"]return\s*\w+\s*[\'\"];\s*return\s+\w+;\s*\};")
    l = constant_function_regex1.findall(js)
    for i in l:
        function_name = re.search("var\s+([^=]+)", i).group(1)
        var_args_equal_value_functions.append(function_name)
        js = js.replace(i, "")
        # 替换全文
        a = function_name
        js = re.sub("%s\(([^\)]+)\)"%a, r"\1", js)

    # var 无参数 返回常量 函数
    var_no_args_return_constant_functions = []
    """
    var Qh_ = function() {
            'return Qh_';
            return ';';
        };
    """
    constant_function_regex2 = re.compile("""
            var\s+[^=]+=\s*function\(\)\{\s*
                [\'\"]return\s*\w+\s*[\'\"];\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
                \};
            """,
            re.X)
    l = constant_function_regex2.findall(js)
    for i in l:
        function_name = re.search("""
            var\s+([^=]+)=\s*function\(\)\{\s*
                [\'\"]return\s*\w+\s*[\'\"];\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
                \};
            """,
            i,
            re.X)
        var_no_args_return_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b = function_name.groups()
        all_var["%s()"%a] = b

    # 无参数 返回常量 函数
    no_args_return_constant_functions = []
    """
    function ZP_() {
            'return ZP_';
            return 'E';
        }
    """
    constant_function_regex3 = re.compile("""
            function\s*\w+\(\)\s*\{\s*
                [\'\"]return\s*[^\'\"]+[\'\"];\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*
        """,
        re.X)
    l = constant_function_regex3.findall(js)
    for i in l:
        function_name = re.search("""
            function\s*(\w+)\(\)\s*\{\s*
                [\'\"]return\s*[^\'\"]+[\'\"];\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*
        """,
        i,
        re.X)
        no_args_return_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b = function_name.groups()
        all_var["%s()"%a] = b


    # 无参数 返回常量 函数 中间无混淆代码
    no_args_return_constant_sample_functions = []
    """
    function do_() {
            return '';
        }
    """
    constant_function_regex3 = re.compile("""
            function\s*\w+\(\)\s*\{\s*
                return\s*[\'\"][^\'\"]*[\'\"];\s*
            \}\s*
        """,
        re.X)
    l = constant_function_regex3.findall(js)
    for i in l:
        function_name = re.search("""
            function\s*(\w+)\(\)\s*\{\s*
                return\s*[\'\"]([^\'\"]*)[\'\"];\s*
            \}\s*
        """,
        i,
        re.X)
        no_args_return_constant_sample_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a,b = function_name.groups()
        all_var["%s()"%a] = b

    # 字符串拼接时使无参常量函数
    """
    (function() {
                'return sZ_';
                return '1'
            })()
    """
    constant_function_regex6 = re.compile("""
            \(function\(\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*[\'\"][^\'\"]*[\'\"];?
            \}\)\(\)
        """,
        re.X)
    l = constant_function_regex6.findall(js)
    for i in l:
        function_name = re.search("""
            \(function\(\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*([\'\"][^\'\"]*[\'\"]);?
            \}\)\(\)
        """,
        i,
        re.X)
        js = js.replace(i, function_name.group(1))

    # 字符串拼接时使用返回参数的函数
    """
    (function(iU__) {
                'return iU_';
                return iU__;
            })('9F')
    """
    constant_function_regex6 = re.compile("""
            \(function\(\w+\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*\w+;
            \}\)\([\'\"][^\'\"]*[\'\"]\)
        """,
        re.X)
    
    l = constant_function_regex6.findall(js)
    for i in l:
        function_name = re.search("""
            \(function\(\w+\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*\w+;
            \}\)\(([\'\"][^\'\"]*[\'\"])\)
        """,
        i,
        re.X)
        js = js.replace(i, function_name.group(1))

    # 获取所有变量
    var_regex = "var\s\w+_='[^']*';"

    for var in  re.findall(var_regex, js):
        if 'span' in var:
            continue
        var_name, var_value = var[4:-1].split('=')
        var_value = var_value.strip("\'\"").strip()
        if "(" in var_value:
            var_value = ";"
        all_var[var_name] = var_value

    # 注释掉 此正则可能会把关键js语句删除掉
    #js = re.sub(var_regex, "", js)

    for var_name, var_value in all_var.items():
        js = js.replace(var_name, var_value)

    js = re.sub("[\s+']", "", js)

    string_region = re.findall("([a-f][a-f0-9]{3})(,|\w{2}_)", js)
    string_region = [x[0] for x in string_region]

    string_str = string_region[-1]

    # 从 字符串密集区域后面开始寻找索引区域
    index_m = re.search("([\d,]+(;[\d,]+)+)", js[js.find(string_str) + len(string_str):])

    string_list = string_region
    index_list = index_m.group(1).split(";")

    _word_list = []
    for word_index_list in index_list:
        _word = ""
        word_index_list = [int(word_index_list)]
        for word_index in word_index_list:
            _word += string_list[word_index]
        _word_list.append(_word)
    return _word_list


def get_complete_text_autohome(text, chinese_mapping):
    text = re.findall('<div\sclass="text-con"[\w\W]*?</div>', text)[-1]
    _types_info = defaultdict(list)
    types = re.findall('hs_kw(\d+_[^\'\"]+)', text)
    for item in types:
        idx, type = item.split("_")
        _types_info[type].append(idx)
    # 获取混淆字符个数
    types = {type: len(set(value)) for type, value in _types_info.items()}

    js_list = re.findall("<script>(\(function[\s\S]+?)\(document\);</script>", text.encode("utf8"))[-1]
    js_list = [js_list]
    type_charlist = {}
    for js in js_list:
        for _type in types:
            if _type in js:
                break
        else:
            continue
        if not js:
            continue
        try:
            char_list = get_char(js, types[_type])
            char_list = [chinese_mapping[w] for w  in char_list]
        except Exception as e:
            traceback.print_exc()
            continue
        type_charlist.update({_type: char_list})
    def char_replace(m):
        index = int(m.group(1))
        typ = m.group(2)
        char_list = type_charlist.get(typ, [])
        if not char_list:
            return m.group()
        char = char_list[index]
        return char

    text = re.sub("<span\s*class=[\'\"]hs_kw(\d+)_([^\'\"]+)[\'\"]></span>", char_replace, text)
    text = re.sub("<style[^>]+?>[\s\S]+?</style>", "", text)
    text = re.sub("<script[^>]?>[\s\S]+?</script>", "", text)

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
    ttf_url = 'http:' + re.search('url(.*\.ttf)', response.text).group(0)[5:]
    ttf_filename = ttf_url.split('/')[-1]
    if not os.path.exists(ttf_filename):
        commands.getstatusoutput('wget %s' % (ttf_url))
    font = TTFont(ttf_filename)
    chinese_mapping = {}

    for index, code in enumerate(font.getGlyphOrder()[1:]):
        chinese_mapping[code[3:].lower()] = word[index]
    if os.path.exists(ttf_filename):
        commands.getstatusoutput('rm %s' % (ttf_filename))
    text = get_complete_text_autohome(response.text, chinese_mapping)
    text = BeautifulSoup(text, 'lxml').get_text("\n",strip=True)
    parse_logger.error(text)
    ret = {"k_source":"autohome"}
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='gbk')
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

    ret['k_content'] = BeautifulSoup(text, 'lxml').get_text("\n",strip=True)

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
