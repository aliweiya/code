package com.example.springboot_mybatis.controller;

import com.example.springboot_mybatis.entity.UserEntity;
import com.example.springboot_mybatis.mapper.UserMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
public class IndexController {

    Logger logger = LoggerFactory.getLogger(getClass());

    private UserMapper userMapper;

    @Autowired
    public void setUserMapper(UserMapper userMapper){
        this.userMapper = userMapper;
    }

    @ResponseBody
    @RequestMapping("/hello")
    public String hello(){
        return "hello world!";
    }

    // 如果不加ResponseBody，则会报错would dispatch back to the current handler URL
    @ResponseBody
    @RequestMapping("/user/query")
    public List<UserEntity> query(String type){
        if(type != null)
            logger.debug(type);
        return userMapper.getUser(type);
    }

    @ResponseBody
    @RequestMapping("/user/add")
    public String addUser(String name, int age, String type){
        userMapper.insert(new UserEntity(name, age, type));
        return "success";
    }
}
