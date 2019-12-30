package com.itheima.test;

import com.itheima.domain.Account;
import com.itheima.service.IAccountService;
import config.SpringConfiguration;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;

/*
 * 使用junit提供的 `@RunWith` 注解把原有的main方法替换成Spring提供的
 * 告知spring运行，spring和ioc创建是基于xml还是注解的，并说明位置
 *  locations: 指定xml文件位置
 *  classes: 注解类所在位置
 *
 *  spring 5.x要求junit 4.12及以上
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes= SpringConfiguration.class)
public class AccountServiceTestWithSprintTest {

    @Autowired
    private IAccountService as;

    @Test
    public void testFindAll(){
        List<Account> accounts = as.findAllAccount();
        for(Account account: accounts){
            System.out.println(account);
        }
    }

    @Test
    public void testFindOne(){
        Account account = as.findAccountById(1);
        System.out.println(account);
    }

    @Test
    public void testSave(){
        Account account = new Account("ddd", 3.2f);
        as.saveAccount(account);
    }

    @Test
    public void testUpdate(){
        Account account = as.findAccountById(4);
        account.setMoney(2345f);
        as.updateAccount(account);
    }

    @Test
    public void testDelete(){
        as.deleteAccount(4);
    }
}
