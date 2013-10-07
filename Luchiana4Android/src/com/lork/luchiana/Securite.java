package com.lork.luchiana;

import android.util.Log;

public class Securite {
	
	public static String vigenere(String phrase, String clef, String operation){
		String sortie = "";
		//1=chiffre 2=dechiffre
		//Log.d("LUCHIANA", phrase);
		int i = 0;
		for(int j=0; j < phrase.length();j++){
			if(operation=="1"){
				int positionAscii = phrase.charAt(j);
				int positionAsciiClef = clef.charAt(i);
				int caract=(positionAscii+positionAsciiClef)%256;
				sortie=sortie+String.valueOf(Character.toChars(caract));
				i=i+1;
				if(i>clef.length()-1){
					i=0;
				}
			}
			else{
				int positionAscii = phrase.charAt(j);
				//Log.d("LUCHIANA", String.valueOf(positionAscii));
				int positionAsciiClef = clef.charAt(i);
				int caract=(positionAscii-positionAsciiClef)%256;
				//Log.d("LUCHIANA", String.valueOf(caract));
				sortie=sortie+String.valueOf(Character.toChars(caract));
				//Log.d("LUCHIANA", sortie);
				i=i+1;
				if(i>clef.length()-1){
					i=0;
				}
			}
		}
		return sortie;
	}
/*
 * ord=place table ascii
 * chr=recup caractère selon place table ascii
 * 
def vigenere(phrase,clef,operation):											+
    #1=chiffre 2=dechiffre														+
    sortie, i = "", 0															+
    for caract in phrase:   #parcours de la chaine a traiter					+
        if operation == "1":    #chiffrement									+
            sortie = sortie + chr((ord(caract) + ord(clef[i])) % 256)
            i = i + 1   #parcours de la cle										+
            if i > len(clef) - 1:												+	
                i = 0   #fin de cle atteinte, on repart au debut				+
        elif operation == "2":  #dechiffrement									+
            sortie = sortie + chr((ord(caract) - ord(clef[i])) % 256)
            i = i + 1															+
            if i > len(clef) - 1:												+
                i = 0															+
    return sortie
*/
}
