package com.springinaction;

public class BraveKnight implements Knight{
    private Quest quest;

    public BraveKnight(Quest quest){
        // Quest被注入进来
        this.quest = quest;
    }

    public void embarkOnQuest(){
        quest.embark();
    }
}