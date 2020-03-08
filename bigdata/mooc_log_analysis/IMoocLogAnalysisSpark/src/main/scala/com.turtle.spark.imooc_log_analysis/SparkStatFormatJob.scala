package com.turtle.spark.imooc_log_analysis

import com.ggstar.util.ip.IpHelper
import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}
import org.apache.spark.{SparkConf, SparkContext};


object SparkStatFormatJob {

  def main(args: Array[String]): Unit ={
    val appName = "stat_format"
    val conf = new SparkConf().setAppName(appName).set("spark.hadoop.validateOutputSpecs", "false")
    val sc = new SparkContext(conf);

    val struct = StructType(
      Array(
        StructField("url", StringType),
        StructField("cmsType", StringType),
        StructField("flow", IntegerType),
        StructField("ip", StringType),
        StructField("city", StringType),
        StructField("time", StringType)
      )
    )

    val accessRDD = sc.textFile("hdfs://172.16.86.133:8020/turtle/imooc_log_analysis/inputs/access.20161111.log")

    accessRDD.map(line =>{
      val splits = line.split(" ");
      val ip = splits(0);
      var city = "";
      try{
        city =  IpHelper.findRegionByIp(ip);
      }
      catch{
        case e: Exception =>
      }
      val time = splits(3).substring(1);
      var url = splits(6);
      if(url.contains("?")){
        url = url.substring(0, url.indexOf("?"))
      }
      var cmsType =""
      try{
        cmsType = url.substring(1, url.substring(1).indexOf("/"))
      }
      catch{
        case e:Exception =>
      }
      val flow = splits(9);
      //      Row(url, cmsType, flow, ip, city, time);
      String.format("%s\t%s\t%s\t%s\t%s\t%s", url, cmsType, flow, ip, city, time)
    }).saveAsTextFile("hdfs://172.16.86.133:8020/turtle/imooc_log_analysis/outputs_spark/")
  }
}
