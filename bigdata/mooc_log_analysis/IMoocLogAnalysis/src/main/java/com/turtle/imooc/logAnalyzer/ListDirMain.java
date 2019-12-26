package com.turtle.imooc.logAnalyzer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.LocatedFileStatus;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.RemoteIterator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

/*
 * Run by hadoop jar  IMoocLogAnalysis-1.0-SNAPSHOT.jar com.turtle.imooc.ListDirMain
 */
public class ListDirMain {

    private static final Logger logger = LoggerFactory.getLogger(ListDirMain.class);

    public static void main(String[] args) throws IOException {

        Configuration conf = new Configuration();
        // 不能写 127.0.0.1
        conf.set("fs.defaultFS", "hdfs://172.16.86.133:8020/");
        FileSystem fs = FileSystem.get(conf);

        // path, recursive
        RemoteIterator<LocatedFileStatus> files = fs.listFiles(new Path("/user/turtle"), false);
        while(files.hasNext()){
            LocatedFileStatus lfs = files.next();
            Path filePath = lfs.getPath();
            String fileName = filePath.getName();
            logger.info(fileName);
        }
    }
}
