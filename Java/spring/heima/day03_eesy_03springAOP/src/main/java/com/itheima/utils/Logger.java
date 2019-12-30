package com.itheima.utils;

import org.aspectj.lang.ProceedingJoinPoint;

public class Logger {

    /**
     * 打印日志，并且让其在切入点方法之前执行（切入点方法就是业务层方法）
     */
    public void beforePrintLog(){
        System.out.println("前置通知 beforePringLog 开始记录日志");
    }

    public void afterReturningPrintLog(){
        System.out.println("后置通知 afterReturningPrintLog 开始记录日志");
    }

    public void afterThrowingPrintLog(){
        System.out.println("异常通知 afterThrowingPrintLog 开始记录日志");
    }

    public void afterPrintLog(){
        System.out.println("最终通知 afterPrintLog 开始记录日志");
    }

    /**
     * 环绕通知
     *
     * Spring框架为我们提供了一个接口 `ProceedingJoinPoint`，该接口有一个方法`proceed()`，此方法相当于明确调用切入点方法
     * 该接口可以作为环绕通知的方法参数，在程序执行时，Spring会提供该接口的实现类给我们使用
     */
    public Object aroundPrintLog(ProceedingJoinPoint pjp){
        Object rtValue = null;
        try{
            Object[] args = pjp.getArgs();

            System.out.println("aroundPrintLog 记录日志 前置");
            rtValue = pjp.proceed(args);
            System.out.println("aroundPrintLog 记录日志 后置");
            return rtValue;
        }catch(Throwable e){
            System.out.println("aroundPrintLog 记录日志 异常");
            throw new RuntimeException(e);
        }finally {
            System.out.println("aroundPrintLog 记录日志 最终");
        }
    }
}
