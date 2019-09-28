package com.mr_turtle.hadoop_demo;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

public class main {
    public static void main(String... args)throws IOException, URISyntaxException, InterruptedException {
        // upload a file to HDFS
        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "hdfs://192.168.5.22:9000/");
        FileSystem fs = FileSystem.get(conf);
        // 指定用户
        fs = FileSystem.get(new URI("hdfs://ip:9000/"), conf, "hadoop");

        // 上传文件
        fs.copyFromLocalFile(new Path("/home/hadoop/test.txt"), new Path("hdfs://ip:9000/test.txt"));
        // 下载文件
        fs.copyToLocalFile(new Path("hdfs://ip:9000/test.txt"), new Path("/home/hadoop/test.txt"));
        // 创建文件夹
        fs.mkdirs(new Path("aaa/bbb/ccc"));
        // 删除文件
        fs.delete(new Path("/aa"), true);
        // 重命名
        fs.rename(new Path("/aa/bb/c"), new Path("/aa/bb/d"));
        // ls
        RemoteIterator<LocatedFileStatus> files = fs.listFiles(new Path("/"), true);

        while(files.hasNext()){
            LocatedFileStatus lfs = files.next();
            Path filePath = lfs.getPath();
            String fileName = filePath.getName();
            System.out.println(fileName);
        }

        // 文件夹
        FileStatus[] listStatus = fs.listStatus(new Path("/"));
        for(FileStatus status:listStatus){
            String name = status.getPath().getName();
            System.out.println(name + (status.isDirectory() ? "is dir": "is file"));
        }
    }
}


