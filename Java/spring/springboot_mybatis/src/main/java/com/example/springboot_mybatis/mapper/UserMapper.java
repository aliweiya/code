package com.example.springboot_mybatis.mapper;

import com.example.springboot_mybatis.entity.UserEntity;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserMapper {
    List<UserEntity> getUser(@Param(value="type") String userType);

    @Insert("insert into user(name, age, type) values(#{name}, #{age}, #{type})")
    void insert(UserEntity userEntity);
}
