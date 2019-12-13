package com.example.myapplication;

import android.os.Bundle;
import android.util.Log;
import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

import java.util.List;
import java.util.Map;

public class XposedInit implements IXposedHookLoadPackage {

    private final String TAG = "douyin#################";

    @Override
    public void handleLoadPackage(final XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable{
        Log.i(TAG, loadPackageParam.packageName);
        if("com.ss.android.ugc.aweme".equals(loadPackageParam.packageName)){
            try{
                XposedHelpers.findAndHookMethod("com.ss.sys.ces.a", loadPackageParam.classLoader, "leviathan",
                        String.class, List.class, boolean.class, new XC_MethodHook() {
                            @Override
                            protected void beforeHookedMethod(MethodHookParam param) throws Throwable{
                                Log.i(TAG, "before call leviathan");
                            }

                            @Override
                            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                                try{
                                    String arg0 = (String) param.args[0];
                                    if(arg0.contains("user_id")){
                                        StringBuilder sb = new StringBuilder();
                                        List arg1 = (List)param.args[1];
                                        if(arg1 != null){
                                            Log.i(TAG, String.format("%d", arg1.size()));
                                            for(int i=0; i<arg1.size();i++){
                                                Log.i(TAG, arg1.get(i).toString());

                                                Log.i(TAG, (String)XposedHelpers.callMethod(arg1.get(i), "a"));
                                                Log.i(TAG, (String)XposedHelpers.callMethod(arg1.get(i), "b"));
                                                sb.append(arg1.get(i) + ",");
                                            }
                                        }
                                        else{
                                            Log.i(TAG, "args1 is NULL");
                                        }
                                        Log.i(TAG, "args0: " + param.args[0]);

                                        Log.i(TAG, "args1: " + sb.toString());
                                        Log.i(TAG, "args2: " + param.args[2]);
                                        Log.i(TAG, "result: " + param.getResult());
                                    }
                                }catch(Exception e){
                                    Log.i(TAG, "hook error: " + Log.getStackTraceString(e));
                                }
                            }
                        });
            }catch(Exception e){
                Log.e(TAG, Log.getStackTraceString(e));
            }
            try{
                XposedHelpers.findAndHookMethod("com.ss.android.common.applog.u", loadPackageParam.classLoader, "a",
                        Map.class, boolean.class, new XC_MethodHook() {
                            @Override
                            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                                Map<String, String> map = (Map<String, String>)param.args[0];
                                for(Map.Entry<String, String> entry: map.entrySet()){
                                    Log.i(TAG, String.format("before call common param %s: %s", entry.getKey(), entry.getValue()));
                                }
                            }

                            @Override
                            protected void afterHookedMethod(MethodHookParam param)throws Throwable{
                                Map<String, String> map = (Map<String, String>)param.args[0];
                                for(Map.Entry<String, String> entry: map.entrySet()){
                                    Log.i(TAG, String.format("after call common param %s: %s", entry.getKey(), entry.getValue()));
                                }
                            }
                        });
            }catch(Exception e){
                Log.i(TAG, Log.getStackTraceString(e));
            }
            XposedHelpers.findAndHookMethod("com.ss.android.common.applog.UserInfo",
                    loadPackageParam.classLoader, "getUserInfo", int.class,
                    String.class, String[].class, new XC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                            try{
                                StringBuilder sb = new StringBuilder();
                                String[] ary = (String[])param.args[2];
                                if(ary != null){
                                    for(int i=0; i<ary.length;i++){
                                        sb.append(ary[i] + ":");
                                    }
                                }
                                Log.i(TAG, "args0: " + param.args[0]);
                                Log.i(TAG, "args1: " + param.args[1]);
                                Log.i(TAG, "args2: " + sb);
                                Log.i(TAG, "result: " + param.getResult());
                            }catch(Exception e){
                                Log.i(TAG, "hook error: " + Log.getStackTraceString(e));
                            }
                        }
                    });

            XposedHelpers.findAndHookMethod("com.ss.android.common.applog.UserInfo", loadPackageParam.classLoader,
                    "initUser", String.class, new XC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                            super.afterHookedMethod(param);
                            Log.i(TAG, "initUser" + param.args[0]);
                        }
                    });


        }
        else if(loadPackageParam.packageName.equals("com.example.myapplication")){
            XposedHelpers.findAndHookMethod("com.example.myapplication.MainActivity", loadPackageParam.classLoader,
                    "onCreate", Bundle.class, new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param)throws Throwable{
                            super.beforeHookedMethod(param);
                        }

                        @Override
                        protected void afterHookedMethod(MethodHookParam param)throws Throwable{
//                            Class c = loadPackageParam.classLoader.loadClass("com.example.myapplication.MainActivity");
//                            Field field = c.getDeclaredField("tv");
//                            field.setAccessible(true);
//                            XposedBridge.log("Test");
//                            TextView tv = (TextView)field.get(param.thisObject);
//                            tv.setText("贪玩蓝月11");
                            super.afterHookedMethod(param);
                        }
                    });
        }
    }
}
