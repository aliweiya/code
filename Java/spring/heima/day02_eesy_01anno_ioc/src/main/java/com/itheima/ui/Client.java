package com.itheima.ui;

import com.itheima.service.IAccountService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
/*
 * 模拟一个表现层，用于调用业务层
 */
public class Client {
    /*
     * 获取Spring 的IOC核心容器，并根据id获取对象
     */
    public static void main(String[] args) {
        // 立即加载
        ApplicationContext ac = new ClassPathXmlApplicationContext("bean.xml");
        // 根据id获取对象
        IAccountService as = (IAccountService)ac.getBean("accountServiceImpl");

    }
}
