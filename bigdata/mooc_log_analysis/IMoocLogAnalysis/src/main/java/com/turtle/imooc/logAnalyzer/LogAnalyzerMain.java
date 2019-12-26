package com.turtle.imooc.logAnalyzer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

public class LogAnalyzerMain extends Configured implements Tool {
    private static final Logger logger = LoggerFactory.getLogger(LogAnalyzerMain.class);

    public int run(String[] args) throws IOException, ClassNotFoundException, InterruptedException {

        Configuration conf = getConf();

        Job job = Job.getInstance(conf);

        job.setJarByClass(LogAnalyzerMain.class);

        job.setMapperClass(LogAnalyzerMapper.class);
        job.setMapOutputKeyClass(LongWritable.class);
        job.setMapOutputValueClass(LogBean.class);

        job.setReducerClass(LogAnalyzerReducer.class);
        job.setOutputKeyClass(NullWritable.class);
        job.setOutputValueClass(LogBean.class);

        FileInputFormat.setInputPaths(job, new Path("/turtle/imooc_log_analysis/inputs"));
        FileOutputFormat.setOutputPath(job, new Path("/turtle/imooc_log_analysis/outputs"));

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        // 不能写 127.0.0.1
        conf.set("fs.defaultFS", "hdfs://172.16.86.133:8020/");
        ToolRunner.run(conf, new LogAnalyzerMain(), args);


    }
}
