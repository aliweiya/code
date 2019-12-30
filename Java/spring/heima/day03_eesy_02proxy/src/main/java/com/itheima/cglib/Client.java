package com.itheima.cglib;

import com.itheima.proxy.IProducer;
import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

/**
 * 模拟一个消费者
 */
public class Client {

    public static void main(String[] args) {

        final Producer producer = new Producer();
        /**
         * 基于子类的动态代理
         *
         * 使用Enhancer类中的creat方法
         *
         * 被代理类不能是final类
         *
         * 参数：
         *  - Class：被代理对象字节码
         *  - Callback：用于增强，一般实现子接口 MethodInterceptor
         */
        Producer cglibProducer = (Producer)Enhancer.create(producer.getClass(), new MethodInterceptor() {
            /**
             *
             * @param o
             * @param method
             * @param objects
             * @param methodProxy 当前方法的被代理对象
             * @return
             * @throws Throwable
             */
            public Object intercept(Object o, Method method, Object[] objects, MethodProxy methodProxy) throws Throwable {
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

        cglibProducer.saleProduct(12000f);
    }
}
