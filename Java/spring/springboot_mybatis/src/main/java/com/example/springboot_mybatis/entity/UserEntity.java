package com.example.springboot_mybatis.entity;

import java.io.Serializable;

public class UserEntity implements Serializable {
    private Integer id;
    private String name;
    private Integer age;
    private String type;

    public UserEntity(Integer id, String name, Integer age, String type) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.type = type;
    }

    public UserEntity(String name, Integer age, String type) {
        this.name = name;
        this.age = age;
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public Integer getAge() {
        return age;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Integer getId() {
        return id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
