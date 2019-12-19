package com.spring_in_action.spittr.data;

import com.spring_in_action.spittr.Spittle;

import java.util.List;

public interface SpittleRepository {
    List<Spittle> findSpittles(long max, int count);
}
