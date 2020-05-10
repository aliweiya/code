package com.luban.service;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

@FeignClient("SERVER-POWER")
public interface PowerFeignClient {

    @GetMapping("/getPower")
    public Object getPower();
}
