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

    @Autowired
    RestTemplate restTemplate;

    @RequestMapping("/getUser")
    public R getUser() {
        Map<String, Object> map = new HashMap<>();
        map.put("key", "用户数据");
        return R.success("返回成功", map);
    }

    @RequestMapping("/getPower")
    public R getPower() {
        return R.success("操作成功", restTemplate.getForObject("http://localhost:6000/getPower", Object.class));
    }
}
