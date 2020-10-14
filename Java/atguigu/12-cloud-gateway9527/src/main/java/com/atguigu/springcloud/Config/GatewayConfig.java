package com.atguigu.springcloud.Config;

import com.atguigu.springcloud.filter.MyLogGatewayFilter;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder routeLocatorBuilder) {
        RouteLocatorBuilder.Builder routes = routeLocatorBuilder.routes();
        routes.route("path_route",
                // 访问国内则会转发到uri
                r -> r.path("/guonei").uri("https://news.baidu.com/guinei")).build();

        return routes.build();
    }

    @Bean
    public GlobalFilter customFilter() {
        return new MyLogGatewayFilter();
    }
}
