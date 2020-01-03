package com.turtle.spark.imooc_log_analysis

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.functions.{sum, count, when, col, lit, round}
import org.apache.spark.sql.{Row, SQLContext}
import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.hive.HiveContext

object TaoBaoRecommend {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("yarn-cluster").setAppName("TaoBaoRecommend")
    val sc = new SparkContext(conf)

    val sqlContext = new HiveContext(sc)

//    val sqlContext = new SQLContext(sc)
    import sqlContext.implicits._

    val behavior_type_mapping = Map(
      "1" -> "click",
      "2" -> "fav",
      "3" -> "cart",
      "4" -> "pay"
    )

    val taobaoSchema = StructType(Array(
      // name, dataType, nullable
      StructField("user_id", StringType, false),
      StructField("item_id", StringType, false),
      StructField("behavior_type", StringType, true),
      StructField("user_geohash", StringType, true),
      StructField("item_category", StringType, true),
      StructField("time", StringType, true),
      StructField("date", StringType, true),
      StructField("hour", StringType, true)
    ))
    val rdd = sqlContext.read.format("csv").
      option("header", "true").
      schema(taobaoSchema).
      load("hdfs://172.16.86.133:8020/turtle/taobao_recommand/dataset/tianchi_mobile_recommend_train_user.csv").
      map(row => {
        val user_id = row.getAs[String]("user_id")
        val item_id = row.getAs[String]("item_id")
        val behavior_type = behavior_type_mapping(row.getAs[String]("behavior_type"))
        val user_geohash = row.getAs[String]("user_geohash")
        val item_category = row.getAs[String]("item_category")
        val time = row.getAs[String]("time")
        val date_hour = time.split(" ")
        Row(user_id, item_id, behavior_type, user_geohash, item_category, time, date_hour(0), date_hour(1))
      })

    var df = sqlContext.createDataFrame(rdd, taobaoSchema)

    // 地理位置信息经过加密处理，且大部分缺失，直接去掉
    df = df.drop("user_geohash").drop("time")

    df.registerTempTable("taobao_recommend")

    // 统计pv（page view，访问量）
    df.filter("behavior_type = 'click'").count
    sqlContext.sql("select COUNT(behavior_type) from taobao_recommend where behavior_type='click'").show()

    // 日均访问量
    df.filter("behavior_type = 'click'").groupBy("date").count().orderBy("date").show()
    sqlContext.sql("select date, count(1) from taobao_recommend where behavior_type='click' group by(date) order by (date) desc").show()

    // uv（unique view，用户量）
    df.select("user_id").distinct().count()
    sqlContext.sql("select count(distinct user_id) from taobao_recommend").show()

    // 有购买行为的用户数量
    df.filter("behavior_type = 'pay'").select("user_id").distinct().count()
    sqlContext.sql("select count(distinct user_id) from taobao_recommend where behavior_type = 'pay'").show()

    // 用户的购物情况
    // the user_id is added automatically
    df.select("user_id", "behavior_type").groupBy("user_id").agg(
      count("behavior_type").as("total_behavior"),
      sum(when($"behavior_type" === "click", 1)).as("total_click"),
      sum(when($"behavior_type" === "cart", 1)).as("total_cart"),
      sum(when($"behavior_type" === "fav", 1)).as("total_fav"),
      sum(when($"behavior_type" === "pay", 1)).as("total_pay")).orderBy(col("total_behavior").desc).write.saveAsTable("user_shopping_info")

    sqlContext.sql("select user_id, count(behavior_type), " +
      "sum(case when behavior_type='click' then 1 else 0 end), " +
      "sum(case when behavior_type='fav' then 1 else 0 end), " +
      "sum(case when behavior_type='cart' then 1 else 0 end), " +
      "sum(case when behavior_type='pay' then 1 else 0 end) " +
      "from taobao_recommend group by user_id order by count(behavior_type) desc").
      toDF("user_id", "total", "click", "fav", "cart", "pay").
      registerTempTable("user_behavior")

    // 用户行为转化为漏斗图
    df.select("user_id", "behavior_type").agg(
      lit("1").as("pv"),
      round(sum(when($"behavior_type" === "fav", 1)) / sum(when($"behavior_type" === "click", 1)), 2).as("pv_to_fav"),
      round(sum(when($"behavior_type" === "cart", 1)) / sum(when($"behavior_type" === "click", 1)), 2).as("pv_to_cart"),
      round(sum(when($"behavior_type" === "pay", 1)) / sum(when($"behavior_type" === "click", 1)), 2).as("pv_to_pay")
    ).show()
    sqlContext.sql("select round(sum(click) / sum(total), 2), round(sum(fav) / sum(total), 2), round(sum(cart) / sum(total), 2), round(sum(pay) / sum(total), 2) from user_behavior").show()
  }
}
