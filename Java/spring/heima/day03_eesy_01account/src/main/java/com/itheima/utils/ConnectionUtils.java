package com.itheima.utils;


import javax.sql.DataSource;
import java.sql.Connection;

/**
 * 从数据源获取一个连接，并实现和线程绑定
 */
public class ConnectionUtils {
    private ThreadLocal<Connection> tl = new ThreadLocal<Connection>();

    private DataSource dataSource;

    public void setDataSource(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /**
     * 获取当前线程连接
     * @return
     */
    public Connection getThreadConnection(){
        try{
            // 先从ThreadLocal获取
            Connection conn = tl.get();
            // 判断是否有连接
            if(conn == null){
                // 从数据源获取
                conn = dataSource.getConnection();
                tl.set(conn);
            }
            return conn;
        }catch(Exception e){
            throw new RuntimeException(e);
        }
    }

    /**
     * 关闭连接后将连接和ThreadLocal解绑
     */
    public void remove(){
        tl.remove();
    }
}
