package com.turtle.spark.imooc_log_analysis

import org.apache.spark.{SparkConf, SparkContext}
;

object SparkStatFormatJob {

  def main(args: Array[String]): Unit ={
    val appName = "stat_format"
    val master = "yarn"
    val conf = new SparkConf().setAppName(appName).setMaster(master);
    val sc = new SparkContext(conf);

    val access = sc.textFile("hdfs://172.16.86.133:8020/turtle/imooc_log_analysis/inputs/access.20161111.log")

    access.map(line =>{
      val splits = line.split(" ");
      val ip = splits(0);
      val time = splits(3).substring(1);
      var url = splits(6);
      if(url.contains("?")){
        url = url.substring(0, url.indexOf("?"))
      }
      val flow = splits(9);
      time + "\t" + url + "\t" + flow + "\t" +  ip;
    }).saveAsTextFile("hdfs://172.16.86.133:8020/turtle/imooc_log_analysis/spark_outputs/")
  }
}
