package com.example.macos.starthack19_bosh;

import android.content.Intent;
import android.os.AsyncTask;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
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
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private TextToSpeech mTTS;
    private Button educationalMode;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        educationalMode = findViewById(R.id.educationalMode);
        educationalMode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, EducationalActivity.class));
            }
        });


        mTTS = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int result = mTTS.setLanguage(Locale.ENGLISH);
                    try{
                        URL url = new URL("http://130.82.236.114:5002/messages");

                        new MainActivity.MsgAsynTask().execute(url);
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

    }

    private void speak(String message) {
        mTTS.setPitch(1);
        mTTS.setSpeechRate(1);

        mTTS.speak(message, TextToSpeech.QUEUE_FLUSH, null);
    }

    public String readJSON(URL url){
        JSONParser parser = new JSONParser();
        String message = "";

        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));

            JSONObject notification = (JSONObject) parser.parse(in);
            if(notification.containsKey("weather")){
                message = (String) notification.get("weather");
                speak(message);
                Log.d("message: " ,message);
            }else{
                Log.d("No msg", "NULL");
            }

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
            String msg = readJSON(urls[0]);
            publishProgress(msg);
            return msg;
        }

        protected void onPostExecute(String result) {}

        @Override
        protected void onPreExecute() {}

        @Override
        protected void onProgressUpdate(String... result) {
            TextView mTxtView;
            mTxtView = findViewById(R.id.weather);
            mTxtView.setText(result[0]);
        }

    }
}
