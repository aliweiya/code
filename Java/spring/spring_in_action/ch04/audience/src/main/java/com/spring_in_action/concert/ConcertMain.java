package com.spring_in_action.concert;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class ConcertMain{
    public static void main(String[] args)throws Exception{
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(ConcertConfig.class);
        Performance concert = applicationContext.getBean(Performance.class);
        concert.perform();
        applicationContext.close();
    }
}