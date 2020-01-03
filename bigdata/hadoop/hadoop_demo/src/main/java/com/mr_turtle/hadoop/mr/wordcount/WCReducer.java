package com.mr_turtle.hadoop.mr.wordcount;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class WCReducer extends Reducer<Text, LongWritable, Text, LongWritable> {

    // 框架处理完成后，将所有kv缓存起来，进行分组，传递一个组，调用一次reduce方法
    // <hello, {1, 1, ...}
    @Override
    protected  void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
        long count = 0;
        for(LongWritable value: values){
            count += value.get();
        }

        // 输出统计结果
        context.write(key, new LongWritable(count));
    }
}
