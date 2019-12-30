package com.itheima.dao.impl;

import com.itheima.dao.IAccountDao;
import com.itheima.domain.Account;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.support.JdbcDaoSupport;

import java.util.List;

public class AccountDaoImpl extends JdbcDaoSupport implements IAccountDao {
    public Account findAccountById(Integer accountId) {
        List<Account> accountList = getJdbcTemplate().query("select * from account where id=?", new BeanPropertyRowMapper<Account>(Account.class), accountId);
        return accountList.isEmpty()? null: accountList.get(0);
    }

    public Account findAccountByName(String accountName) {
        List<Account> accountList = getJdbcTemplate().query("select * from account where name=?", new BeanPropertyRowMapper<Account>(Account.class), accountName);
        if(accountList.isEmpty()){
            return null;
        }
        else if(accountList.size() > 1){
            throw new RuntimeException("结果集不唯一！");
        }
        return accountList.get(0);
    }

    public void updateAccount(Account account) {
        getJdbcTemplate().update("update account set name=?, money=? where id=?", account.getName(), account.getMoney(), account.getId());
    }


}
