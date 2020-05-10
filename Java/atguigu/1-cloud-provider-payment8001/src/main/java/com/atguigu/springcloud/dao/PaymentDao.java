package com.atguigu.springcloud.dao;

import com.atguigu.springcloud.entities.Payment;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

// 推荐@Mapper，不建议@Repository
@Mapper
public interface PaymentDao {
    // 返回数字，大于1表示插入成功
    int create(Payment payment);

    Payment getPaymentById(@Param("id") Long id);
}
