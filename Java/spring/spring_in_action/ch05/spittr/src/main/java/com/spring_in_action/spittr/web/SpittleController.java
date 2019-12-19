package com.spring_in_action.spittr.web;

import com.spring_in_action.spittr.Spittle;
import com.spring_in_action.spittr.data.SpittleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

import static org.springframework.web.bind.annotation.RequestMethod.POST;

@Controller
@RequestMapping("/spittles")
public class SpittleController {
    private SpittleRepository spittleRepository;

    private static final String MAX_LONG_AS_STRING = "10000";

    @Autowired
    public SpittleController(SpittleRepository spittleRepository){
        this.spittleRepository = spittleRepository;
    }

    // Spring MVC 在调用方法前会创建一个–隐含的模型对象作为模型数据的存储容器。
    // 如果方法的入参为 Map 或 Model 类型，Spring MVC 会隐含模型的引用传递给这些入参。
    // 在方法体内，开发者可以通过这个入参对象访问到模型中的所有数据，也可以向模型中添加新的属性数据。
//    @RequestMapping(method= RequestMethod.GET)
//    public String spittles(Model model){
//        model.addAttribute(spittleRepository.findSpittles(Long.MAX_VALUE, 20));
//        return "spittles";
//    }

//    @RequestMapping(method=RequestMethod.GET)
//    public List<Spittle> spittles(@RequestParam("max") long max,
//                                  @RequestParam("count") int count){
//        return spittleRepository.findSpittles(max, count);
//    }

    /*
     * 提供默认参数
     */
    @RequestMapping(method=RequestMethod.GET)
    public List<Spittle> spittles(@RequestParam(value="max", defaultValue = MAX_LONG_AS_STRING) long max,
                                  @RequestParam(value="count", defaultValue = "20") int count){
        return spittleRepository.findSpittles(max, count);
    }

//    @RequestMapping(value="/{spittleId}", method = RequestMethod.GET)
//    public String spittle(@PathVariable("spittleId")long spittleId,
//                          Model model){
//        model.addAttribute(spittleRepository.findOne(spittleId));
//        return "spittle";
//    }

//    @RequestMapping(value="register", method=POST)
//    public String processRegistration(Spittle spitter){
//        spittleRepository.save(spitter);
//        return "redirect:/spitter/" + spitter.getUserName();
//    }
}
