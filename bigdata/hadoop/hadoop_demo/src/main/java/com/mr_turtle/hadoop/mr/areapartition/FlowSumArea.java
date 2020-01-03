package com.mr_turtle.hadoop.mr.areapartition;

import com.mr_turtle.hadoop.mr.flowsum.FlowBean;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.StringUtils;

import java.io.IOException;
import java.util.HashMap;

/*
 * 对流量原始日志进行统计，将不同省份的用户统计结果输出到不同文件
 * 需要改造两个机制：
 * 1. 改造分区的逻辑，自定义partitioner
 * 2. 自定义reducer task的并发任务数
 */
public class FlowSumArea {
    public static class FlowSumAreaMapper extends Mapper<LongWritable, Text, Text, FlowBean> {
        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] fields = StringUtils.split(line, '\t');

            String phoneNB = fields[1];
            long u_flow = Long.parseLong(fields[7]);
            long d_flow = Long.parseLong(fields[8]);

            context.write(new Text(phoneNB), new FlowBean(phoneNB, u_flow, d_flow));
        }
    }

    public static class FlowSumAreaReducer extends Reducer<Text, FlowBean, Text, FlowBean>{
        @Override
        protected void reduce(Text key, Iterable<FlowBean> values, Context context) throws IOException, InterruptedException {
            long up_flow_counter = 0;
            long d_flow_counter = 0;

            for(FlowBean bean: values){
                up_flow_counter += bean.getUp_flow();
                d_flow_counter += bean.getD_flow();
            }

            context.write(key, new FlowBean(key.toString(), up_flow_counter, d_flow_counter));
        }
    }



    public static class FlowSumAreaPartitioner<KEY, VALUE> extends Partitioner<KEY, VALUE>{
       private static HashMap<String, Integer> areaCode = new HashMap<String, Integer>();

        static {
            areaCode.put("130", 1);
            areaCode.put("132", 2);
        }

        @Override
        public int getPartition(KEY key, VALUE value, int numPartition){
            int areaCoder = areaCode.get(key.toString().substring(0, 3)) == null ? 3: areaCode.get(key.toString().substring(0, 3));
            return areaCoder;
        }
    }

    public static void main(String... args) throws IOException, InterruptedException, ClassNotFoundException{
        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf);

        // 指定jar
        job.setJarByClass(FlowSumArea.class);

        // 设置Mapper和Reducer
        job.setMapperClass(FlowSumAreaMapper.class);
        job.setReducerClass(FlowSumAreaReducer.class);

        // 设置partitioner
        job.setPartitionerClass(FlowSumAreaPartitioner.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(FlowBean.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FlowBean.class);

        // reduce任务并发数
        job.setNumReduceTasks(3);

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.waitForCompletion(true);
    }
}
