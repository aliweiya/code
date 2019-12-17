package com.spring_in_action.soundsystem;

import org.springframework.stereotype.Component;

import java.util.List;

public class BlankDisc implements CompactDisc{
    public void setTitle(String title){
        this.title = title;
    }

    public void setArtist(String artist){
        this.artist = artist;
    }

    public String getTitle(){
        return title;
    }

    public String getArtist(){
        return artist;
    }

    public void setTracks(List tracks){
        this.tracks = tracks;
    }

    public List<String> getTracks(){
        return tracks;
    }

    public void playTrack(int i){
        System.out.println(tracks.get(i));
    }

    public void play(){}

    private String title;
    private String artist;
    private List<String> tracks;
}
