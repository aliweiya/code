package com.atguigu.springcloud.controller;

import com.atguigu.springcloud.entities.CommonResult;
import com.atguigu.springcloud.entities.Payment;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

@RestController
@Slf4j
public class PaymentController {

    /**
     * 不加@RequestBody会插入NULL
     */
    @PostMapping(value="/payment/create")
    public CommonResult create(@RequestBody  Payment payment) {
        return new CommonResult(200, "插入数据库成功");
    }

    @GetMapping(value = "/payment/get/{id}")
    public CommonResult getPaymentById(@PathVariable("id") Long id) {
        return new CommonResult(200, "查询成功");
    }
}
