package com.itheima.domain;

import java.io.Serializable;

/*
 * 账户的实体类
 */
public class Account implements Serializable {
    private Integer id;
    private String name;
    private Float money;

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Float getMoney() {
        return money;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setMoney(Float money) {
        this.money = money;
    }

    public Account(String name, Float money) {
        this.name = name;
        this.money = money;
    }

    @Override
    public String toString() {
        return "Account{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", money=" + money +
                '}';
    }
}
