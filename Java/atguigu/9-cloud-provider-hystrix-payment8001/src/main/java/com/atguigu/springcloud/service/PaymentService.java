package com.atguigu.springcloud.service;

public interface PaymentService {
    String paymentInfo(Integer id);

    String paymentInfoFallTimeout(Integer id);
}
