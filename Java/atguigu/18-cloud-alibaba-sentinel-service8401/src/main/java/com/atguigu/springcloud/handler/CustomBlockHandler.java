package com.atguigu.springcloud.handler;

import com.alibaba.csp.sentinel.slots.block.BlockException;
import com.atguigu.springcloud.entities.CommonResult;

public class CustomBlockHandler {
    public static CommonResult handleException(BlockException exception) {
        return new CommonResult(444, "自定义错误处理");
    }
}
