package com.example.macos.starthack19_bosh;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import org.json.JSONException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;

public class ListActivity extends AppCompatActivity {

    private ListView listView;
    private ArrayAdapter<String> stringArrayAdapter;
    private ArrayList<String> mistakesArrayList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list);

        Bundle stringArrayList = getIntent().getExtras();
        ArrayList<String> list = stringArrayList.getStringArrayList("all mistakes");

//        System.out.print("here is the list: " + list.get(1));


        listView = findViewById(R.id.listView);

        mistakesArrayList= new ArrayList<String>();
            mistakesArrayList.add("Turn off high beam");
        mistakesArrayList.add("You have exceeded the speed limit");

        stringArrayAdapter = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_list_item_1,mistakesArrayList);
        listView.setAdapter(stringArrayAdapter);
        mistakesArrayList.add("here we go");
        stringArrayAdapter.notifyDataSetChanged();
    }
}
