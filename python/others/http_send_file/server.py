# -*- coding: utf-8 -*-

import os
import BaseHTTPServer

""" 发送文件 """


class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):

        # self.send_response(403)
        # self.end_headers()
        # return
        self.do_POST()

    def do_POST(self):
        filename = self.path
        if filename == "/":
            if os.path.exists("csv.zip"):
                os.remove("csv.zip")

            os.system(
                """zip -r csv.zip car_brand.csv car_brand_tasks.csv car_series.csv car_series_tasks.csv car_type.csv car_type_tasks.csv""")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(open("csv.zip", "rb").read())

        else:
            self.send_response(404)

if __name__ == "__main__":

    print "Server start..."
    srvr = BaseHTTPServer.HTTPServer(('0.0.0.0', 50003), MyHTTPRequestHandler)
    srvr.serve_forever()
