package com.turtle.imooc.logAnalyzer;

import com.turtle.imooc.logAnalyzer.LogBean;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class LogAnalyzerReducer extends Reducer<LongWritable, LogBean, NullWritable, LogBean> {
    private NullWritable out = NullWritable.get();
    @Override
    protected void reduce(LongWritable key, Iterable<LogBean> values, Context context) throws IOException, InterruptedException {
        for(LogBean bean: values){
            context.write(out, bean);
        }
    }
}
