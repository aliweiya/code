package com.turtle.spark.imooc_log_analysis

import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}

object AccessConvertUtil {
  val struct = StructType(
    Array(
      StructField("url", StringType),
      StructField("cmsType", StringType),
      StructField("cmsId", StringType),
      StructField("flow", IntegerType),
      StructField("ip", StringType),
      StructField("city", StringType),
      StructField("time", StringType)
    )
  )

  def parseLog(log: String) ={

  }
}
