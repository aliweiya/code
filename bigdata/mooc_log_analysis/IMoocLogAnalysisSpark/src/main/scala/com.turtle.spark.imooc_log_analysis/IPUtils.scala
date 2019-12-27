package com.turtle.spark.imooc_log_analysis

import com.ggstar.util.ip.IpHelper

object IPUtils {
  def getCity(ip:String) = {
    IpHelper.findRegionByIp(ip)
  }

  def main(args: Array[String]): Unit = {
    println(getCity("111.202.145.130"))
  }
}
