package com.mr_turtle.hadoop.mr.ii;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.StringUtils;

import java.io.IOException;

public class InverseIndexStepOne {

    public static class StepOneMapper extends Mapper<LongWritable, Text, Text, LongWritable> {
        @Override
        protected void map(LongWritable key, Text value, Context context)throws IOException, InterruptedException {
            String line = value.toString();
            String[] fields = StringUtils.split(line, '\t');

            // 从切片获取文件信息
            FileSplit fileSplit = (FileSplit) context.getInputSplit();

            String fileName = fileSplit.getPath().getName();

            for(String field:fields){
                // 封装k-v输出
                context.write(new Text(field + "-->" + fileName), new LongWritable(1));
            }
        }
    }

    public static class StepOneReducer extends Reducer<Text, LongWritable, Text, LongWritable>{
        @Override
        protected void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException{
            long counter = 0;
            for(LongWritable value: values){
                counter += value.get();
            }

            context.write(key, new LongWritable(counter));
        }
    }

    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf);
        job.setJarByClass(InverseIndexStepOne.class);

        job.setMapperClass(StepOneMapper.class);
        job.setReducerClass(StepOneReducer.class);


        Path output = new Path(args[1]);
        FileSystem fs = FileSystem.get(conf);
        if(fs.exists(output)){
            fs.delete(output, true);
        }

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, output);


        System.exit(job.waitForCompletion(true) ? 0 :1);
    }
}
