package com.atguigu.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @Configuration 指定当前类是一个配置类，替代Spring配置文件
 */
@Configuration
public class MyAppConfig {

    /**
     * @Bean 将方法的返回值添加到容器中，默认名就是方法名
     * @return
     */
    @Bean
    public HelloService helloService(){
        return new HelloService();
    }
}
