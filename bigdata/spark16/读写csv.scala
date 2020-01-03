object ReadCSV {
  def main(args: Array[String]): Unit = {

    val conf = new SparkConf()
      .setMaster("local[2]")
      .setAppName("ReadCSV")
    val sc = new SparkContext(conf)


    val sqlContext = new org.apache.spark.sql.SQLContext(sc)

    val customSchema = StructType(Array(
      StructField("year", IntegerType, true),
      StructField("make", StringType, true),
      StructField("model", StringType, true),
      StructField("comment", StringType, true),
      StructField("blank", StringType, true)))
    val df = sqlContext.read.format("csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .load("hdfs://192.168.137.251:8020/data/cars.csv")

    val selectedData = df.select("year", "model")
    selectedData.write
      .format("com.databricks.spark.csv")
      .option("header", "true")
      .save("hdfs://192.168.137.251:8020/data/newcars3.csv")
      df.printSchema
    sc.stop()
  }
}