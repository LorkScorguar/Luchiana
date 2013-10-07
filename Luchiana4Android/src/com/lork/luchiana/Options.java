package com.lork.luchiana;


import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;

public class Options extends Activity {

	private SharedPreferences prefs;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_options);
		ActionBar actionBar = getActionBar();
		actionBar.setDisplayHomeAsUpEnabled(true);
		actionBar.setHomeButtonEnabled(true);
		
		prefs = getSharedPreferences("Luchiana", Context.MODE_PRIVATE);
		String server = prefs.getString("server", "");
		int port = prefs.getInt("port", 0);
		String user = prefs.getString("user", "");
		String password = prefs.getString("password", "");
		
		EditText serveur = (EditText)findViewById(R.id.EditTextServeur);
		EditText eport = (EditText)findViewById(R.id.EditTextPort);
		EditText utilisateur = (EditText)findViewById(R.id.EditTextUtilisateur);
		EditText passe = (EditText)findViewById(R.id.editTextPassword);
		
		serveur.setText(server);
		eport.setText(String.valueOf(port));
		utilisateur.setText(user);
		passe.setText(password);
		
		
		final Button button = (Button)findViewById(R.id.buttonSave);
		button.setOnClickListener(new View.OnClickListener() {
    		public void onClick(View v) {
				EditText serveur = (EditText)findViewById(R.id.EditTextServeur);
				EditText eport = (EditText)findViewById(R.id.EditTextPort);
				EditText utilisateur = (EditText)findViewById(R.id.EditTextUtilisateur);
				EditText passe = (EditText)findViewById(R.id.editTextPassword);
				
				String server = serveur.getText().toString();
				int port = Integer.parseInt(eport.getText().toString());
				String user = utilisateur.getText().toString();
				String password = passe.getText().toString();
				
				prefs = getSharedPreferences("Luchiana", Context.MODE_PRIVATE);
				SharedPreferences.Editor editor = prefs.edit();
				editor.putString("server", server);
				editor.putInt("port", port);
				editor.putString("user", user);
				editor.putString("password", password);
	    		editor.commit();
    		}
    	});
		
	}
	
	@Override
    public boolean onOptionsItemSelected(MenuItem menuItem)
    {       
        startActivity(new Intent(Options.this,MainActivity.class)); 
        return true;
    }
}
