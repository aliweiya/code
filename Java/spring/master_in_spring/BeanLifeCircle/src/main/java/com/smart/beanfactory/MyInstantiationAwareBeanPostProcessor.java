package com.smart.beanfactory;

import org.springframework.beans.PropertyValues;
import org.springframework.beans.factory.config.InstantiationAwareBeanPostProcessorAdapter;

import java.beans.PropertyDescriptor;

public class MyInstantiationAwareBeanPostProcessor extends InstantiationAwareBeanPostProcessorAdapter {
    // call before instantiate
    public Object postProcessBeforeInstantiation(Class beanClass, String beanName){
        if("car".equals(beanName)){
            System.out.println("InstantiationAware BeanPostProcessor.postProcessBeforeInstantiation");
        }
        return null;
    }

    // call after instantiate
    public boolean postProcessAfterInstantiation(Object bean, String beanName){
        if("car".equals(beanName)){
            System.out.println("InstantiationAware BeanPostProcessor.postProcessAfterInstantiation");
        }
        return true;
    }

    // call when set value
    public PropertyValues postProcessPropertyValues(
            PropertyValues pvs, PropertyDescriptor[] pds, Object bean, String beanName){
        if("car".equals(beanName)){
            System.out.println("Instantiation AwareBeanPostProcessor.postProcessPropertyValues");
        }
        return pvs;
    }
}
