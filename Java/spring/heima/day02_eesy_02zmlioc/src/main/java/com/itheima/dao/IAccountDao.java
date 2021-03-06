package com.itheima.dao;

import com.itheima.domain.Account;

import java.util.List;

/*
 * 账户的持久层
 */
public interface IAccountDao {
    /*
     * 查询所有
     */
    List<Account> findAllAccount();

    /*
     * 查询一个
     */
    Account findAccountById(Integer accountId);

    /*
     * 保存操作
     */
    void saveAccount(Account account);

    /*
     * 更新
     */
    void updateAccount(Account account);

    /*
     * 删除
     */
    void deleteAccount(Integer accountId);
}