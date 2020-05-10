package com.luban.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class PowerController {

    @GetMapping("/getPower")
    public Object getPower() {
        Map<String,  Object> map = new HashMap<>();
        map.put("key", "power");
        return map;
    }
}
