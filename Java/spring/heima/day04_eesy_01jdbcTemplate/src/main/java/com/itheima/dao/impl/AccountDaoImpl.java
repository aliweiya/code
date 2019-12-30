package com.itheima.dao.impl;

import com.itheima.dao.IAccountDao;
import com.itheima.domain.Account;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.List;

/**
 * 账户的持久层实现类
 */
public class AccountDaoImpl implements IAccountDao {
    private JdbcTemplate jdbcTemplate;

    public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Account findAccountById(Integer accountId) {
        List<Account> accountList = jdbcTemplate.query("select * from account where id=?", new BeanPropertyRowMapper<Account>(Account.class), accountId);
        return accountList.isEmpty()? null: accountList.get(0);
    }

    public Account findAccountByName(String accountName) {
        List<Account> accountList = jdbcTemplate.query("select * from account where name=?", new BeanPropertyRowMapper<Account>(Account.class), accountName);
        if(accountList.isEmpty()){
            return null;
        }
        else if(accountList.size() > 1){
            throw new RuntimeException("结果集不唯一！");
        }
        return accountList.get(0);
    }

    public void updateAccount(Account account) {
        jdbcTemplate.update("update account set name=?, money=?, where id=?", account.getName(), account.getMoney(), account.getId());
    }
}
