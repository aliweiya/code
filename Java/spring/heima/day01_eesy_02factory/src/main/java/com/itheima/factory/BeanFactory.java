package com.itheima.factory;


import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

/*
 * Bean在计算机中，有可重用组件的含义。
 *
 * JavaBean不等于实体类，用java语言编写的可重用组件
 *
 * factory用于创建Service和Dao对象
 *
 * 需要一个配置文件配置Service和Dao
 *
 * 读取配置文件，通过反射创建对象
 * properties相对于xml读取和解析更简单
 */
public class BeanFactory {
    private static Properties props;

    // 定义Map，用于存储要创建的对象，称为容器
    private static Map<String, Object> beans;

    // 使用静态代码块为Properties为对象赋值
    static {
        try{
            // 实例化
            props = new Properties();
            // 获取properties文件的流对象
            InputStream in = BeanFactory.class.getClassLoader().getResourceAsStream("bean.properties");
            props.load(in);
            // 实例化容器
            beans = new HashMap<String, Object>();
            // 取出配置文件中所有的Key
            Enumeration keys = props.keys();
            while(keys.hasMoreElements()){
                // 取出每个key
                String key = keys.nextElement().toString();
                String beanPath = props.getProperty(key);
                Object value = Class.forName(beanPath).newInstance();
                // 存入容器
                beans.put(key, value);
            }

        }catch(Exception e){
            throw new ExceptionInInitializerError("初始化properties失败！");
        }
    }

    /*
     * 根据Bean的名称获取Bean对象
     */
    // public static Object getBean(String beanName){
    //    Object bean = null;
    //     try{
    //         String beanPath=props.getProperty(beanName);
    //         // 每次都调用默认构造函数创建
    //         bean = Class.forName(beanPath).newInstance();
    //     }catch(Exception e){
    //         e.printStackTrace();
    //     }
    //     return bean;
    // }

    /*
     * 根据名字获取bean
     */
    public static Object getBean(String beanName){
        return beans.get(beanName);
    }
}
