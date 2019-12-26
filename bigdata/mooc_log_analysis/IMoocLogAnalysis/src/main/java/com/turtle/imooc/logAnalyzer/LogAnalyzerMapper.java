package com.turtle.imooc.logAnalyzer;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.util.StringUtils;

import java.io.IOException;

/*
 * mapred代表的是hadoop旧API，而mapreduce代表的是hadoop新的API
 * KEYIN, VALUEIN, KEYOUT, VALUEOUT
 * 前两个参数一般不需要动，偏移量，文件内容，
 */
public class LogAnalyzerMapper extends Mapper<LongWritable, Text, LongWritable, LogBean> {
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        try{
            String line = value.toString();
            String[] fields = StringUtils.split(line, ' ');
            String clientIP = fields[0];
            String date = fields[3];
            date = date.substring(1);
            int flow = Integer.parseInt(fields[9]);
            String url = fields[6];

            if (url.contains("?")){
                url = url.substring(0, url.indexOf('?'));
            }

            context.write(key, new LogBean(date, url, flow, clientIP));
        }catch(Exception e){

        }
    }
}
