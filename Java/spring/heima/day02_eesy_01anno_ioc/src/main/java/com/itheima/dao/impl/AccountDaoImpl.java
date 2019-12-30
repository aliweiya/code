package com.itheima.dao.impl;

import com.itheima.dao.IAccountDao;
import org.springframework.stereotype.Component;

@Component
public class AccountDaoImpl implements IAccountDao {
    public void save() {
        System.out.println("saved account");
    }
}
