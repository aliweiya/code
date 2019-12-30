package com.itheima.test;

import com.itheima.service.IAccountService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = "classpath:beanWithFactory.xml")
public class AccountServiceTestWithFactory {

    @Autowired
    @Qualifier("proxyAccountService")
    private IAccountService as;

    @Test
    public void testTranfer(){
        as.transfer("aaa", "bbb", 100f);
    }
}
