package com.turtle.imooc.logAnalyzer;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class LogBean implements Writable {
    // 访问日期
    private String date;
    // 访问的URL
    private String url;
    // 流量
    private int flow;
    // 客户端IP
    private String clientIP;

    // for reflection
    public LogBean(){}

    public LogBean(String date, String url, int flow, String clientIP) {
        this.date = date;
        this.url = url;
        this.flow = flow;
        this.clientIP = clientIP;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public int getFlow() {
        return flow;
    }

    public void setFlow(int flow) {
        this.flow = flow;
    }

    public String getClientIP() {
        return clientIP;
    }

    public void setClientIP(String clientIP) {
        this.clientIP = clientIP;
    }

    public void write(DataOutput output) throws IOException{
        output.writeUTF(date);
        output.writeUTF(url);
        output.writeInt(flow);
        output.writeUTF(clientIP);
    }

    public void readFields(DataInput in) throws IOException{
        date = in.readUTF();
        url = in.readUTF();
        flow = in.readInt();
        clientIP = in.readUTF();
    }

    @Override
    public String toString() {
        return String.format("%s %s %d %s", date, url, flow, clientIP);
    }
}
