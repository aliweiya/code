package com.itheima.service.impl;

import com.itheima.service.IAccountService;
import org.springframework.stereotype.Service;

@Service("accountService")
public class AccountServiceImpl implements IAccountService {
    public void saveAccount() {
        System.out.println("save executed!");
    }

    public void updateAccount(int i) {
        System.out.println("update executed!");
    }

    public int deleteAccount() {
        System.out.println("delete executed!");
        return 0;
    }
}
