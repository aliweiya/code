package com.itheima.service.impl;

import com.itheima.dao.IAccountDao;
import com.itheima.dao.impl.AccountDaoImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/*
 * 账户的业务层实现类
 */
@Component
@Scope("prototype")
public class AccountServiceImpl implements com.itheima.service.IAccountService {

    @Autowired
    @Qualifier("accountDao")
    private IAccountDao adao;

    public void saveAccount() {
        adao.save();
    }
}
