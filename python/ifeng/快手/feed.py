import hashlib

import requests

url = "http://api.gifshow.com/rest/n/feed/hot?"

salt = "382700b563f4"

headers = {
    "User-Agent": "kwai-android",
    "Connection": "keep-alive",
    "Accept-Language": "zh-cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "api.gifshow.com",
    "Accept-Encoding": "gzip",
}


def sig(param, data):
    def parse(s):
        for item in s.split('&'):
            k, v = item.split('=')
            to_sign[k] = v

    to_sign = {}
    parse(param)
    parse(data)

    _list = []
    for k, v in to_sign.items():
        if 'sig' != k:
            _list.append("{}={}".format(k, v))

    _list = sorted(_list)

    string = "".join(_list) + salt
    _sign = hashlib.md5(string.encode('utf-8')).hexdigest()
    return _sign


def feed():
    param = "appver=6.5.5.9591"
    data = "client_key=3c2cd3f3"
    data = data + '&sig=' + sig(param, data)
    resp = requests.post(url + param, data=data, headers=headers)
    return resp


if __name__ == '__main__':
    resp = feed()
    json_data = resp.json()
    for item in json_data['feeds']:
        print(item['caption'])