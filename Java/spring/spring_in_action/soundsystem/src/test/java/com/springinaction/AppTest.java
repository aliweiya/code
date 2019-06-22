package com.springinaction;

import static junit.Assert.*;

import junit.Test;
import junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;


// 测试时自动创建Spring的应用上下文
@RunWith(SpringJUnit4ClassRunner.class)
// 需要在CDPlayerConfig中加载配置
// 因为CDPlayerCofnig类中包含了@ComponentScan，因此最终的应用上下文中应该包含CompactDisc bean
@ContextConfiguration(classes=CDPlayerConfig.class)
public class AppTest{
    @Autowired
    private CompactDisc cd;

    @Test
    public void cdShouldNotBeNull(){
        assertNotNull(cd);
    }
}
