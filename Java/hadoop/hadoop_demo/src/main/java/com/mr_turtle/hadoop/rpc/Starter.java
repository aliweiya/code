package com.mr_turtle.hadoop.rpc;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.ipc.RPC;
import org.apache.hadoop.ipc.Server;

import java.io.IOException;
import java.net.InetSocketAddress;

interface LoginServiceInterface{
    public static final long versionID=1;
    public String login(String username, String password);
}

class LoginServiceImpl implements LoginServiceInterface{
    public String login(String username, String password){
        return username + "logged in successfully";
    }
}

public class Starter {
    public  static  void main(String... args) throws IOException {
        RPC.Builder builder = new RPC.Builder(new Configuration());
        builder.setBindAddress("127.0.0.1")
                .setPort(10000)
                .setProtocol(LoginServiceInterface.class)
                .setInstance(new LoginServiceImpl());
        Server server = builder.build();
    }
}


class LoginController {
    public static void main(String... args) throws IOException {
        LoginServiceInterface proxy = RPC.getProxy(LoginServiceInterface.class, 1L, new InetSocketAddress("127.0.0.0.1", 10000), new Configuration());
        String result = proxy.login("username", "password");
    }
}