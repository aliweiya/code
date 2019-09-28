package com.mr_turtle.hadoop.mr.ii;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

public class InverseIndexStepTwo {
    public static class StepTwoMapper extends Mapper<LongWritable, Text, Text, Text> {
        @Override
        protected void map(LongWritable key, Text value, Context context)throws IOException, InterruptedException {
            String line = value.toString();
            String[] fields = StringUtils.split(line, '\t');

            String[] wordAndFilename = StringUtils.split(fields[0], "-->");
            String word = wordAndFilename[0];
            String fileName = wordAndFilename[1];

            long count = Long.parseLong(fields[1]);
            context.write(new Text(word), new Text(fileName + "-->" + count));
        }
    }

    public static class StepTwoReducer extends Reducer<Text, LongWritable, Text, Text> {
        @Override
        protected void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException{
            context.write(key, new Text(StringUtils.join(values.iterator(), ",")));
        }
    }

    public static void main(String[] args) throws Exception{
        Configuration conf = new Configuration();
        Job job_one = Job.getInstance(conf);
        job_one.setJarByClass(InverseIndexStepTwo.class);
        job_one.setMapperClass(InverseIndexStepOne.StepOneMapper.class);
        job_one.setReducerClass(InverseIndexStepOne.StepOneReducer.class);

        job_one.setOutputKeyClass(Text.class);
        job_one.setOutputValueClass(LongWritable.class);

        FileInputFormat.setInputPaths(job_one, new Path(args[0]));
        FileOutputFormat.setOutputPath(job_one, new Path(args[1]));

        Job job_two = Job.getInstance(conf);
        job_two.setJarByClass(InverseIndexStepTwo.class);

        job_two.setMapperClass(StepTwoMapper.class);
        job_two.setReducerClass(StepTwoReducer.class);

        job_two.setOutputKeyClass(Text.class);
        job_two.setOutputValueClass(LongWritable.class);

        FileInputFormat.setInputPaths(job_two, new Path(args[0]));
        FileOutputFormat.setOutputPath(job_two, new Path(args[2]));

        // 先提交job_one
        boolean one_result = job_one.waitForCompletion(true);
        System.exit(job_two.waitForCompletion(true) ? 0 :1);
    }
}
