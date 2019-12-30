package com.itheima.jdbctemplate;

import com.itheima.domain.Account;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

/**
 * JdbcTemplate的最基本用法
 */
public class JdbcTemplateDemo1 {
    public static void main(String[] args) {
//        // 准备数据源
//        DriverManagerDataSource ds = new DriverManagerDataSource();
//        ds.setDriverClassName("com.mysql.jdbc.Driver");
//        ds.setUrl("jdbc:mysql://192.168.9.150:3306/eesy");
//        ds.setUsername("root");
//        ds.setPassword("1234qwerty");
//        // 1. 创建JdbcTempalte对象
//        JdbcTemplate jt = new JdbcTemplate();
//        jt.setDataSource(ds);
//        // 2. 执行操作
//        jt.execute("insert into account(name, money) values('ccc', '1000'");

        ApplicationContext ac = new ClassPathXmlApplicationContext("bean.xml");

        JdbcTemplate jt = ac.getBean("jdbcTemplate", JdbcTemplate.class);
        jt.execute("insert into account(name, money) values('ccc', '1000'");

        // 保存
        jt.update("insert into account(name, money) values(?, ?)", "eee", 3333f);

        // 更新
        jt.update("update account set name=>, money=? where id=?", "test", 1234f, 7);

        // 删除
        jt.update("delete from account where id=?", 8);

        // 查询
        List<Account> accounts = jt.query("select * from account where money > ?", new AccountRowMapper(), 1000);
        for(Account account: accounts){
            System.out.println(account);
        }

        // 查询一行一列（使用聚合函数，但不加group by）
        jt.queryForObject("select count(*) from account where money > ?", Integer.class,1000);
    }
}


class AccountRowMapper implements RowMapper<Account> {
    /**
     * 把结果集映射到Account，然后由Account加到集合中
     * @param resultSet
     * @param i
     * @return
     * @throws SQLException
     */
    public Account mapRow(ResultSet resultSet, int i) throws SQLException {
        Account account = new Account();
        account.setId(resultSet.getInt("id"));
        account.setName(resultSet.getString("name"));
        account.setMoney(resultSet.getFloat("money"));
        return account;
    }
}