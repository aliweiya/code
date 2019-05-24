package com.springinaction;

import org.springframework.context.support.ClassPathXmlApplicationContext;
import com.springinaction.Knight;

public class KnightMain{
    public static void main(String[] args)throws Exception{
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("knights.xml");
        Knight knight = context.getBean(Knight.class);
        knight.embarkOnQuest();
        context.close();
    }
}