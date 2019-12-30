package com.smart;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.*;

public class Car implements BeanFactoryAware, BeanNameAware, InitializingBean, DisposableBean {
    private String brand;
    private String color;
    private int maxSpeed;

    private BeanFactory beanFactory;
    private String beanName;

    public Car(){
        System.out.println("call car()");
    }
    public void setBrand(String brand){
        System.out.println("call setBrand()");
        this.brand = brand;
    }

    public String getColor(){
        return color;
    }

    public void setColor(String color){
        this.color = color;
    }

    public int getMaxSpeed(){
        return maxSpeed;
    }

    public void setMaxSpeed(int maxSpeed){
        this.maxSpeed = maxSpeed;
    }

    public void introduce(){
        System.out.println("brnad: " + brand + "; color: " + color + "; maxSpeed: " + maxSpeed);
    }

    // BeanFactoryAware
    public void setBeanFactory(BeanFactory beanFactory) throws BeansException{
        System.out.println("call BeanFactoryAware.setBeanFactory().");
        this.beanFactory = beanFactory;
    }

    // BeanNameAware
    public void setBeanName(String beanName){
        System.out.println("call BeanNameAware.setBeanName()");
        this.beanName = beanName;
    }

    // InitializingBean
    public void afterPropertiesSet() throws Exception{
        System.out.println("call InitializingBean.afterPropertiesSet().");
    }

    // DisposableBean
    public void destroy() throws Exception{
        System.out.println("call DisposableBean.destroy()");
    }

    // init-method
    public void myInit(){
        System.out.println("call init-method");
        this.maxSpeed = 240;
    }

    // destroy-method
    public void myDestroy(){
        System.out.println("call destroy-method");
    }
}
