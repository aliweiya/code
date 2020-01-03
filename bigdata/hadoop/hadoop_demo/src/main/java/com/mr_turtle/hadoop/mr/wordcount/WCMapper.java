package com.mr_turtle.hadoop.mr.wordcount;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.util.StringUtils;

import java.io.IOException;

/*
 * map和reduce的输入输出数据都是以key-value的形式封装的。
 * 前两个是输入数据的泛型，后两个是输出数据的泛型 Long, String, String, Long
 * 前两个一般不需要修改。key是要处理文本中的起始偏移量；value是这一行的内容
 * hadoop实现了一套自己的序列化机制，效率更高，网络传输更精简
 */
public class WCMapper extends Mapper<LongWritable, Text, Text, LongWritable>{
    // 读一行调用一次
    @Override
    protected void map(LongWritable key, Text value, Context context)throws IOException, InterruptedException {
        // key是要处理文本中的起始偏移量；value是这一行的内容
        // 输出的工具放到了context里
        String line = value.toString();
        String[] words = StringUtils.split(line, ' ');
        for(String word:words){
            context.write(new Text(word), new LongWritable(1));
        }
    }
}
