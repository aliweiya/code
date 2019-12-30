package com.itheima.service.impl;

import com.itheima.dao.IAccountDao;
import com.itheima.domain.Account;
import com.itheima.service.IAccountService;
import com.itheima.utils.TransactionManager;

import java.util.List;

public class AccountServiceImplWithBeanFactory implements IAccountService {
    private IAccountDao accountDao;

    private TransactionManager txManager;

    public void setAccountDao(IAccountDao accountDao) {
        this.accountDao = accountDao;
    }

    public void setTxManager(TransactionManager txManager) {
        this.txManager = txManager;
    }

    public List<Account> findAllAccount() {
        return accountDao.findAllAccount();
    }

    public Account findAccountById(Integer accountId) {
        return accountDao.findAccountById(accountId);
    }

    public void saveAccount(Account account) {
        accountDao.saveAccount(account);
    }

    public void updateAccount(Account account) {
        accountDao.updateAccount(account);
    }

    public void deleteAccount(Integer accountId) {
        accountDao.deleteAccount(accountId);
    }

    /**
     * 转账
     * @param sourceName 转出账户名称
     * @param targetName 转入账户名称
     * @param money      金额
     *
     * 使用ThreadLocal把连接和当前线程绑定
     */
    public void transfer(String sourceName, String targetName, Float money) {
        // 1. 根据名称查询转出账户
        Account source = accountDao.findAccountByName(sourceName);
        // 2. 根据名称查询转入账户
        Account target = accountDao.findAccountByName(targetName);
        // 3. 转出账户减钱
        source.setMoney(source.getMoney() - money);
        // 4. 转入账户加钱
        target.setMoney(target.getMoney() + money);
        // 5. 更新转出账户
        accountDao.updateAccount(source);
        // 6. 更新转入账户
        accountDao.updateAccount(target);

    }
}
