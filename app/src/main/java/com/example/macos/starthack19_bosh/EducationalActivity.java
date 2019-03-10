package com.example.macos.starthack19_bosh;


import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Locale;


public class EducationalActivity extends AppCompatActivity {

    private TextToSpeech mTTS;
    private Button showAll;
    private ArrayList<String> mistakesArrayList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_educational);

        mistakesArrayList = new ArrayList<String>();

        mTTS = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int result = mTTS.setLanguage(Locale.ENGLISH);
                    try{
                        URL url = new URL("http://130.82.236.114:5002/mistakes");

                        new MsgAsynTask().execute(url);
                    }catch (MalformedURLException e){
                        e.printStackTrace();
                    }

                    if (result == TextToSpeech.LANG_MISSING_DATA
                            || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e("TTS", "Language not supported");
                    }
                } else {
                    Log.e("TTS", "Initialization failed");
                }
            }
        });

        showAll = findViewById(R.id.showAll);
        showAll.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(EducationalActivity.this, ListActivity.class);
                intent.putStringArrayListExtra("all mistakes", mistakesArrayList);
                startActivity(intent);
            }
        });
    }

    private void speak(String message) {
        mTTS.setPitch(1);
        mTTS.setSpeechRate(1);

        mTTS.speak(message, TextToSpeech.QUEUE_FLUSH, null);
    }

    public String readJSON(URL url){
        JSONParser parser = new JSONParser();
        String message = "You are doing well, Keep Going :)";
        Log.d("error " ,message);

        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            JSONArray errors = (JSONArray) parser.parse(in);

            if (errors.size()!=0){
                for (int i=0; i<errors.size(); i++){
                    JSONObject mistake = (JSONObject) errors.get(i);
                    mistakesArrayList.add(mistake.toString());

                    String time = (String) mistake.get("time");

                    System.out.println(time);

                    String error = (String) mistake.get("error");
                    message = error;
                    speak(error);
                    System.out.println("errrooooooooooooooooor: " + error);
                }
            }else
                mistakesArrayList.add("there is no mistake");


        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return message;

    }


    @Override
    protected void onDestroy() {
        if (mTTS != null) {
            mTTS.stop();
            mTTS.shutdown();
        }
        super.onDestroy();
    }

    private class MsgAsynTask extends AsyncTask<URL, String, String> {

        @Override
        protected String doInBackground(URL... urls) {
            while (true) {
                try {
                    String msg = readJSON(urls[0]);
                    publishProgress(msg);
                    Thread.sleep(3000);
                } catch (InterruptedException e) {
                    Thread.interrupted();
                }
            }
        }

        protected void onPostExecute(String result) {}

        @Override
        protected void onPreExecute() {}

        @Override
        protected void onProgressUpdate(String... result) {
            TextView mTxtView;
            mTxtView = findViewById(R.id.msgText);
            mTxtView.setText(result[0]);
        }

    }
}
