package com.atguigu.springcloud.controller;

import com.alibaba.csp.sentinel.annotation.SentinelResource;
import com.atguigu.springcloud.entities.CommonResult;
import com.atguigu.springcloud.entities.Payment;
import com.atguigu.springcloud.handler.CustomBlockHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RateLimitController {
    @GetMapping("/rateLimit/customBlockHandler")
    @SentinelResource(value="customBlockHandler", blockHandlerClass = CustomBlockHandler.class, blockHandler = "handleException")
    public CommonResult customBlockHandler() {
        return new CommonResult(200, "客户自定义", new Payment(2020L, "serial001"));
    }
}
