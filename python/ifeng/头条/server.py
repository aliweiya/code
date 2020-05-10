import json
import logging
import os
import time

from multiprocessing import Process

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import tornado.ioloop
import tornado.web

CHROME_DRIVER = 'C:\\Users\\lenovo\\Downloads\\chromedriver_win32\\chromedriver.exe'

port = 8888

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

def background():
    """
    这里通过selenium去访问home页，然后隔一段时间刷新一次，并且不让chrome退出。
    """
    time.sleep(1)
    options = Options()
    # 打开开发者模式，不输出日志
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(CHROME_DRIVER,
                              chrome_options=options,
                              service_args=['--verbose'],
                              service_log_path='chromedriver.log')
    driver.get('http://127.0.0.1:{}/'.format(port))

    while True:
        driver.refresh()
        time.sleep(60)

results = {}

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class SignHandler(tornado.web.RequestHandler):
    """
    接收请求，获取url，计算sign值
    """
    def get(self):
        url = self.get_argument('url')
        if url in results:
            self.write(results[url])
        else:
            results[url] = None
            for i in range(5):
                if results[url] is not None:
                    data = {
                        'result': results[url]
                    }
                    self.write(json.dumps(data))
                    break
                time.sleep(1)
            else:
                self.write('{}')


class BrowserHandler(tornado.web.RequestHandler):
    """
    和浏览器交互，浏览器定期访问get接口，如果有需要计算的url，就返回，否则返回空
    """
    def get(self):
        """返回需要计算sign的url
        """
        for k, v in results.items():
            if v is None:
                data = {
                    'url': k,
                }
                self.write(json.dumps(data))
                break
        self.write('{}')

    def post(self):
        """ 获取计算完的结果
        """
        url = self.get_body_argument('url')
        signed = self.get_body_argument('signed')
        results[url] = signed
        self.write('')


if __name__ == "__main__":
    p = Process(target=background)
    p.start()

    handlers = [
        (r'/', IndexHandler),
        (r'/sign', SignHandler),
        (r'/browser', BrowserHandler),
    ]

    app = tornado.web.Application(handlers=handlers,
                                  template_path='templates',
                                  static_path='statics',
                                  debug=True)
    app.listen(port)
    logging.info('starting server...')
    tornado.ioloop.IOLoop.current().start()
