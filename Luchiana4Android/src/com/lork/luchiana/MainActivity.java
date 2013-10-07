package com.lork.luchiana;

import android.R.menu;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.TextToSpeech.OnInitListener;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;


/**
 * Description
 *
 * @author Catalin Prata
 *         Date: 2/12/13
 */
 
/*
 *TODO
 */
public class MainActivity extends Activity implements OnInitListener {
 
    private ListView mList;
    private ArrayList<String> arrayList;
    private ClientListAdapter mAdapter;
    private TcpClient mTcpClient;
    public static MainActivity instance;
    public TextToSpeech mTts;
    public int status;
    public boolean son;
    private boolean envoie;
    private Menu menu;
 
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        instance = this;
        son=false;
        
        
        //initialisation du TTS
        Intent checkIntent = new Intent();
        checkIntent.setAction(TextToSpeech.Engine.ACTION_CHECK_TTS_DATA);
        startActivityForResult(checkIntent, 0x01);

 
        arrayList = new ArrayList<String>();
 
        final EditText editText = (EditText) findViewById(R.id.editText);
        Button send = (Button) findViewById(R.id.send_button);
 
        //relate the listView from java to the one created in xml
        mList = (ListView) findViewById(R.id.list);
        mAdapter = new ClientListAdapter(this, arrayList);
        mList.setAdapter(mAdapter);
 
        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
            	
            	
            		/*Context context = getApplicationContext();
                	CharSequence text = getString(R.string.warning);
                	int duration = Toast.LENGTH_SHORT;

                	Toast toast = Toast.makeText(context, text, duration);
                	toast.show();
            	*/
            	
            	
	            	envoie=true;
	                String message = editText.getText().toString();
	                if(message.equals("quitter") || message.equals("Quitter")){
	                	if(son==true && status==TextToSpeech.SUCCESS){
	                		mTts.speak("A bientôt!", TextToSpeech.QUEUE_ADD, null);
	                	}
						arrayList.add("-->A bientôt");
						mTcpClient.stopClient();
						mTcpClient = null;
						arrayList.clear();
						mAdapter.notifyDataSetChanged();
						finish();
						System.exit(0);
	                }
	                if(message.equals("Parle!")){
	                	son=true;
	                	envoie=false;
	                }
	                if(message.equals("Tais toi!")){
	                	son=false;
	                	envoie=false;
	                }
	            	//chiffrement
	                //add the text in the arrayList
	                arrayList.add(">"+message);
	 
	                //sends the message to the server
	                if (mTcpClient != null && envoie==true) {
	                    mTcpClient.sendMessage("T",message);
	                }
	 
	                //refresh the list
	                mAdapter.notifyDataSetChanged();
	                editText.setText("");
            	}
            
        });
 
    }
 
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main_menu, menu);
        return true;
    }
 
    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
    	this.menu=menu;
    	menu.getItem(0).setEnabled(true);
        if (mTcpClient != null) {
            // if the client is connected, enable the connect button and disable the disconnect one
            menu.getItem(2).setEnabled(true);
            menu.getItem(1).setEnabled(false);
        } else {
            // if the client is disconnected, enable the disconnect button and disable the connect one
            menu.getItem(2).setEnabled(false);
            menu.getItem(1).setEnabled(true);
        }
 
        return super.onPrepareOptionsMenu(menu);
    }
 
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
        	case R.id.options:
	            Intent intent = new Intent(MainActivity.this,Options.class);
	            startActivity(intent);
	            return true;
            case R.id.connect:
                // connect to the server
                new ConnectTask().execute("");
                return true;
            case R.id.disconnect:
                // disconnect
                mTcpClient.stopClient();
                mTcpClient = null;
                // clear the data set
                arrayList.clear();
                // notify the adapter that the data set has changed.
                mAdapter.notifyDataSetChanged();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
 
    }
 
    public class ConnectTask extends AsyncTask<String, String, TcpClient> {
 
        @Override
        protected TcpClient doInBackground(String... message) {
 
            //we create a TCPClient object and
            mTcpClient = new TcpClient(new TcpClient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    publishProgress(message);
                }
            });
            mTcpClient.run();
 
            return null;
        }
 
        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
 
            //in the arrayList we add the messaged received from server
            arrayList.add(values[0]);
            // notify the adapter that the data set has changed. This means that new message received
            // from server was added to the list
            mAdapter.notifyDataSetChanged();
        }
    }
    
    public static MainActivity getSharedInstance() {
	    return instance;
	}
    
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		if (requestCode == 0x01) {
	        if (resultCode == TextToSpeech.Engine.CHECK_VOICE_DATA_PASS) {
	            // Succès, au moins un moteur de TTS à été trouvé, on l'instancie
	            mTts = new TextToSpeech(this, this);
	            status=TextToSpeech.SUCCESS;
	        } else {
	        	status=TextToSpeech.ERROR;
	            // Echec, aucun moteur n'a été trouvé, on propose à l'utilisateur d'en installer un depuis le Market
	            Intent installIntent = new Intent();
	            installIntent.setAction(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA);
	            startActivity(installIntent);
	        }
		}
       }

	@Override
	public void onInit(int arg0) {
		/*if (status == TextToSpeech.SUCCESS) {
            mTts.speak("Ceci est un test grandeur nature du tutoriel sur l'énonciation de texte.", TextToSpeech.QUEUE_FLUSH, null);
            mTts.speak("Ceci est un deuxième test !", TextToSpeech.QUEUE_ADD, null);
        }*/
    }
}