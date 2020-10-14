package com.atguigu.springcloud.service;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/9")
@FeignClient("CLOUD-PROVIDER-HYSTRIX-PAYMENT")
public interface PaymentService {
    @GetMapping("payment/{id}")
    String paymentInfo(@PathVariable("id") Integer id);

    @GetMapping("payment/timeout/{id}")
    String paymentInfoTimeout(@PathVariable("id") Integer id) ;
}
