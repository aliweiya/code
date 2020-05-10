package com.luban.controller;

import com.luban.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
public class UserController {

    private static final String POWER_URL = "http://SERVER-POWER";

    @Autowired
    RestTemplate restTemplate;


    @RequestMapping("/getUser")
    public R getUser(){
        Map<String,Object> map = new HashMap<>();
        map.put("key","user");

        return R.success("返回成功",map);
    }


    @RequestMapping("/getPower")
    public R getPower(){
        return R.success("操作成功",restTemplate.getForObject(POWER_URL + "/getPower",Object.class));
    }

}
