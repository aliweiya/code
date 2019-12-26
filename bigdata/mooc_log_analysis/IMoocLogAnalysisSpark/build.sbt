resolvers += "bintray-spark-packages" at "https://dl.bintray.com/spark-packages/maven/"

name := "IMoocLogAnalysisSpark"

version := "0.1"

scalaVersion := "2.10.5"

libraryDependencies += "org.apache.spark" %% "spark-core" % "1.6.0"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "1.6.0"

libraryDependencies += "org.apache.poi" % "poi-ooxml" % "3.14"