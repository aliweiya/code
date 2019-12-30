package com.itheima.utils;

/**
 * 事务管理工具类，包含了开启、提交、回滚、关闭
 */
public class TransactionManager {

    private ConnectionUtils connectionUtils;

    public void setConnectionUtils(ConnectionUtils connectionUtils) {
        this.connectionUtils = connectionUtils;
    }

    /**
     * 开启事务
     */
    public void beginTransaction(){
        try{
            connectionUtils.getThreadConnection().setAutoCommit(false);
        }catch(Exception e){
            throw new RuntimeException(e);
        }
    }

    /**
     * 提交事务
     */
    public void commit(){
        try{
            connectionUtils.getThreadConnection().commit();
        }catch(Exception e){
            throw new RuntimeException(e);
        }
    }

    /**
     * 回滚事务
     */
    public void rollback(){
        try{
            connectionUtils.getThreadConnection().rollback();
        }catch(Exception e){
            throw new RuntimeException(e);
        }
    }

    /**
     * 释放连接
     */
    public void release(){
        try{
            // 不是关了，而是还回连接池
            connectionUtils.getThreadConnection().close();
            connectionUtils.remove();
        }catch(Exception e){
            throw new RuntimeException(e);
        }
    }
}
