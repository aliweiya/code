package com.itheima.proxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

/**
 * 模拟一个消费者
 */
public class Client {
    public static void main(String[] args) {
        final Producer producer = new Producer();
        producer.saleProduct(10000f);

        /**
         * 动态代理：
         *   特点：字节码随用随创建，随用随加载
         *   作用：不修改字节码的基础上对方法增强
         *   分类：
         *      - 基于接口的
         *      - 基于子类的
         *
         *   如何创建代理对象：
         *      使用Proxy类中的newProxyInstance方法
         *   要求：
         *      最少实现一个接口，否则不能使用
         *   newProxyInstance方法的参数
         *      ClassLoader：类加载器，是用于加载代理对象字节码的。和被代理对象使用相同的类加载器
         *      Class[]：用于让代理对象和被代理对象有相同方法（实现相同的接口）
         *      InvovationHandler：用于提供增强的代码
         *          它是让我们写如何代理。一般是写接口的实现类，通常是匿名内部类，但不是必须
         *          谁用谁写
         */
        final IProducer producerProxed = (IProducer) Proxy.newProxyInstance(producer.getClass().getClassLoader(), producer.getClass().getInterfaces(), new InvocationHandler() {
            /**
             * 执行被代理对象的任何方法都会经过该方法
             * @param o         代理对象的引用
             * @param method    当前执行的方法
             * @param objects   当前执行方法所需的参数
             * @return          和被代理对象方法有相同的返回值
             * @throws Throwable
             */
            public Object invoke(Object o, Method method, Object[] objects) throws Throwable {
                Object returnValue = null;
                // 获取方法执行参数
                Float money = (Float)objects[0];
                // 判断当前方法是不是销售
                if("saleProduct".equals(method.getName())){
                    returnValue = method.invoke(producer, money * 0.8f);
                }
                return returnValue;
            }
        });
        producerProxed.saleProduct(1000f);

        /**
         * 基于子类的动态代理
         */
    }
}
