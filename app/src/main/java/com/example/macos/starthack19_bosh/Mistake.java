package com.example.macos.starthack19_bosh;

/**
 * Created by macos on 3/10/19.
 */

public class Mistake {
    private String time;
    private String error;

    public Mistake(String time, String error) {
        this.time = time;
        this.error = error;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }
}
