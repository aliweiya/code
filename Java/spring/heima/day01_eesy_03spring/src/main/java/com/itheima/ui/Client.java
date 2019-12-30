package com.itheima.ui;

import com.itheima.dao.IAccountDao;
import com.itheima.service.IAccountService;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.xml.XmlBeanFactory;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;

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
        IAccountService as = (IAccountService)ac.getBean("accountService");
        IAccountDao adao = ac.getBean("accountDao", IAccountDao.class);

        // 延迟加载
        Resource resource = new ClassPathResource("bean.xml");
        BeanFactory factory = new XmlBeanFactory(resource);
        IAccountService asf = (IAccountService)factory.getBean("accountService");
    }
}
