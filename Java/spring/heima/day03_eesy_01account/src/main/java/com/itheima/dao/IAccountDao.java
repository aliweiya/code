package com.itheima.dao;

import com.itheima.domain.Account;

import java.util.List;

/**
 * 账户的持久层
 */
public interface IAccountDao {
    /**
     * 查询所有
     */
    List<Account> findAllAccount();

    /**
     * 查询一个
     */
    Account findAccountById(Integer accountId);

    /**
     * 保存操作
     */
    void saveAccount(Account account);

    /**
     * 更新
     */
    void updateAccount(Account account);

    /**
     * 删除
     */
    void deleteAccount(Integer accountId);

    /**
     * 根据名称查询账户
     * @param accountName
     * @return 如果有唯一的就返回，没有返回null，有多个就抛出异常
     */
    Account findAccountByName(String accountName);

}