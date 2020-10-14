package com.atguigu.springcloud.controller;

import com.atguigu.springcloud.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

@RestController
@RequestMapping("/9")
@Slf4j
public class PaymentController {

    @Resource
    private PaymentService paymentService;

    @GetMapping("payment/{id}")
    public String paymentInfo(@PathVariable("id") Integer id) {
        return paymentService.paymentInfo(id);
    }

    @GetMapping("payment/timeout/{id}")
    public String paymentInfoTimeout(@PathVariable("id") Integer id) {
        return paymentService.paymentInfoFallTimeout(id);
    }
}
