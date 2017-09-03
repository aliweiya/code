# -*- coding: utf-8 -*-

import os
import httplib

"""接收文件"""


def get_csv_file():

    conn = httplib.HTTPConnection("121.41.38.232:50003")
    conn.request(method="POST", url="/")
    response = conn.getresponse()
    if response.status == 200:
        if os.path.exists("csv.zip"):
            os.remove("csv.zip")

        for filename in os.listdir("csv/"):
            os.remove(filename)

        with open("csv.zip", "wb") as f:
            print "Receiving..."
            f.write(response.read())
            print "Received."

        os.system("unzip csv.zip -d csv/")

        os.system(
            "hadoop fs -put ~/c_b_s_t_csv/csv/car_brand.csv hdfs://HA-NameNode/user/mathartsys/datawarehouse_v1/c_brand")

if __name__ == "__main__":
    get_csv_file()
