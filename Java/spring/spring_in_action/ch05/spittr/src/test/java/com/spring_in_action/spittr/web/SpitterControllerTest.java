package com.spring_in_action.spittr.web;

import com.spring_in_action.spittr.data.SpittleRepository;
import org.junit.Test;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.Mockito.mock;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

public class SpitterControllerTest {

    @Test
    public void shouldShowRegisteration() throws Exception{
        SpitterControllerTest controller = new SpitterControllerTest();
        MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build();

        mockMvc.perform(get("/spitter/register"))
                .andExpect(view().name("registerForm"));
    }
}
