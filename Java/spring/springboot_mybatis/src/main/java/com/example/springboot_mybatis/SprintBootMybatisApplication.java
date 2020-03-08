package com.example.springboot_mybatis;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan(value = "com.example.springboot_mybatis.mapper")
public class SprintBootMybatisApplication {

    public static void main(String[] args) {
        SpringApplication.run(SprintBootMybatisApplication.class, args);
    }

}
