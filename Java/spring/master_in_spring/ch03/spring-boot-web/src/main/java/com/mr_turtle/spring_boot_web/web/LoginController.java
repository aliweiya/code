package com.mr_turtle.spring_boot_web.web;

import com.mr_turtle.spring_boot_web.domain.User;
import com.mr_turtle.spring_boot_web.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import java.util.Date;

@RestController
public class LoginController {
    private UserService userService;

    @RequestMapping(value={"/", "/index.html"})
    public ModelAndView loginPage(){
        return new ModelAndView("login");
    }

    @RequestMapping(value="/loginCheck.html")
    public ModelAndView loginCheck(HttpServletRequest request, LoginCommand loginCommand){
        boolean isValidUser = userService.hasMatchUser(loginCommand.getUserName(), loginCommand.getPassword());

        if(!isValidUser){
            return new ModelAndView("log", "error", "用户名或密码错误。");
        }else {
            User user = userService.findUserByUserName(loginCommand
                    .getUserName());
            user.setLastIp(request.getLocalAddr());
            user.setLastVisit(new Date());
            userService.loginSuccess(user);
            request.getSession().setAttribute("user", user);
            return new ModelAndView("main");
        }
    }

    @Autowired
    public void setUserService(UserService userService){
        this.userService = userService;
    }

}
