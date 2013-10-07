package com.lork.luchiana;

import android.content.Context;
import android.content.SharedPreferences;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.widget.Toast;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

 
/**
 * Description
 *
 * @author Catalin Prata
 *         Date: 2/12/13
 */
public class TcpClient {
 
    //public static final String SERVER_IP = "192.168.43.78"; //your computer IP address
    //public static final int SERVER_PORT = 9998;
    // message to send to the server
    private String mServerMessage;
    // sends message received notifications
    private OnMessageReceived mMessageListener = null;
    // while this is true, the server will continue running
    private boolean mRun = false;
    // used to send messages
    private PrintWriter mBufferOut;
    // used to read messages from the server
    private BufferedReader mBufferIn;
    
    private SharedPreferences prefs;
 
    /**
     * Constructor of the class. OnMessagedReceived listens for the messages received from server
     */
    public TcpClient(OnMessageReceived listener) {
        mMessageListener = listener;
    }
 
    /**
     * Sends the message entered by client to the server
     *
     * @param message text entered by client
     */
    public void sendMessage(String type, String message) {
        if (mBufferOut != null && !mBufferOut.checkError()) {
        	message=Securite.vigenere(message,"florent","1");
            mBufferOut.println(type+";"+message+"\n");
            mBufferOut.flush();
        }
    }
 
    /**
     * Close the connection and release the members
     */
    public void stopClient() {
 
        // send mesage that we are closing the connection
        sendMessage("T","close");
 
        mRun = false;
 
        if (mBufferOut != null) {
            mBufferOut.flush();
            mBufferOut.close();
        }
 
        mMessageListener = null;
        mBufferIn = null;
        mBufferOut = null;
        mServerMessage = null;
    }
 
    public void run() {
 
        mRun = true;
        MainActivity activity = MainActivity.getSharedInstance();
        boolean identify = false;
        
        try {
        	prefs = activity.getSharedPreferences("Luchiana", Context.MODE_PRIVATE);
    		String server = prefs.getString("server", "");
    		int port = prefs.getInt("port", 0);
    		String user = prefs.getString("user", "");
    		String password = prefs.getString("password", "");
    		
    		if(server=="" || port==0 || user=="" || password==""){
    			Context context = activity.getApplicationContext();
    			CharSequence text = "Vous devez compléter les informations de connexion";
    			int duration = Toast.LENGTH_SHORT;

    			Toast toast = Toast.makeText(context, text, duration);
    			toast.show();
    		}
            //here you must put your computer's IP address.
            InetAddress serverAddr = InetAddress.getByName(server);
 
            Log.e("TCP Client", "C: Connecting...");
 
            //create a socket to make the connection with the server
            Socket socket = new Socket(serverAddr, port);
            
 
            try {
 
                //sends the message to the server
                mBufferOut = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
 
                //receives the message which the server sends back
                mBufferIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                //gestion de l'authentification
                sendMessage("L", user+";,;"+password);
                mServerMessage = mBufferIn.readLine();
                String[] splitA = mServerMessage.split(";");
            	String messageA = splitA[1];
            	messageA=Securite.vigenere(messageA, "florent", "2");
                if(messageA.equals("identify=1")){
                	identify=true;
                }
                	
                //in this while the client listens for the messages sent by the server
                while (mRun && identify==true) {
 
                    mServerMessage = mBufferIn.readLine();
 
                    if (mServerMessage != null && mMessageListener != null) {
                        //call the method messageReceived from MyActivity class
                    	String[] splits = mServerMessage.split(";");
                    	String message = splits[1];
                    	message=Securite.vigenere(message, "florent", "2");
                        mMessageListener.messageReceived("-->"+message);
                        
                        //on retire le (from thread...) pour le TTS
                        String[] splitTTS = message.split("\\(");
                        if(activity.son==true && activity.status==TextToSpeech.SUCCESS){
                        	activity.mTts.speak(splitTTS[0], TextToSpeech.QUEUE_ADD, null);
                        }
                    }
 
                }
 
                Log.e("RESPONSE FROM SERVER", "S: Received Message: '" + mServerMessage + "'");
 
            } catch (Exception e) {
 
                Log.e("TCP", "S: Error", e);
 
            } finally {
                //the socket must be closed. It is not possible to reconnect to this socket
                // after it is closed, which means a new socket instance has to be created.
                socket.close();
            }
 
        } catch (Exception e) {
 
            Log.e("TCP", "C: Error", e);
 
        }
 
    }
 
    //Declare the interface. The method messageReceived(String message) will must be implemented in the MyActivity
    //class at on asynckTask doInBackground
    public interface OnMessageReceived {
        public void messageReceived(String message);
    }
}
