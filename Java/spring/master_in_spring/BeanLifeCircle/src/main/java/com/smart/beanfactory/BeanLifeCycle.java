package com.smart.beanfactory;

import com.smart.Car;
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.beans.factory.support.DefaultListableBeanFactory;
import org.springframework.beans.factory.xml.XmlBeanDefinitionReader;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;

public class BeanLifeCycle {
    private static void LifeCycleInBeanFactory(){
        // 装配文件并启动容器
        Resource res = new ClassPathResource("spring-smart.xml");
        BeanFactory bf = new DefaultListableBeanFactory();
        XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader((DefaultListableBeanFactory)bf);

        reader.loadBeanDefinitions(res);

        // 向容器中注册 MyBeanPostProcessor 后处理器
        // 后处理器的实际调用顺序和注册顺序无关，通过 org.springframework.core.Ordered接口确定调用顺序。
        ((ConfigurableBeanFactory)bf).addBeanPostProcessor(new MyBeanPostProcessor());

        // 注册 MyInstantiationAwareBeanPostProcessor 后处理器
        ((ConfigurableBeanFactory)bf).addBeanPostProcessor(new MyInstantiationAwareBeanPostProcessor());


        // 第一次从容器中获取car，将触发实例化该Bean，将引起生命周期方法的调用
        Car car1 = (Car)bf.getBean("car");
        car1.introduce();
        car1.setColor("red");

        // 第二次获取car，直接从缓冲区获取
        Car car2 = (Car)bf.getBean("car");

        // 看是否指向同一引用
        System.out.println("car1 == car2:" + (car1 == car2));

        // 关闭容器
        ((DefaultListableBeanFactory)bf).destroySingletons();
    }

    public static void main(String[] args) {
        LifeCycleInBeanFactory();
    }
}
