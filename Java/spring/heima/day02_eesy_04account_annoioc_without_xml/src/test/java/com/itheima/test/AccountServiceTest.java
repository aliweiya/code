package com.itheima.test;

import com.itheima.domain.Account;
import com.itheima.service.IAccountService;
import config.SpringConfiguration;
import org.junit.Before;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.util.List;

public class AccountServiceTest {
    private ApplicationContext ac;
    private IAccountService as;

    @Before
    public void init(){
        ac = new AnnotationConfigApplicationContext(SpringConfiguration.class);
        as = ac.getBean("accountService", IAccountService.class);
    }

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
