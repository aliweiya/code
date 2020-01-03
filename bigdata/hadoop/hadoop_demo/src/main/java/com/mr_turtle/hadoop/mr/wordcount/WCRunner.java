package com.mr_turtle.hadoop.mr.wordcount;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

/*
 * 描述Job
 */
public class WCRunner {
    public static void main(String... args) throws IOException, ClassNotFoundException, InterruptedException {

        System.out.println("fdsfsfs");
        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf);

        // 指定jar
        job.setJarByClass(WCRunner.class);

        // 设置Mapper和Reducer
        job.setMapperClass(WCMapper.class);
        job.setReducerClass(WCReducer.class);

        // 同时对Mapper和Reducer起作用
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        // 如果不同，则分别设置
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(LongWritable.class);

        // 原始数据存放位置
        FileInputFormat.setInputPaths(job, new Path("d:/wc/srcdata/"));
        FileOutputFormat.setOutputPath(job, new Path("d:/wc/destdata"));

        System.out.println("fdsfsfs");
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
