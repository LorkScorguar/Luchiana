import subprocess

def parle(texte):
    proc = subprocess.Popen(["espeak","-vmb-fr4","-q","--pho",texte,"-a","150","-p","80","-k","1","-s","140"],stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(["mbrola","-f","1","-t","1","-l","22000","/usr/share/mbrola/fr4/fr4","-","-.au"],stdin=proc.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc3 = subprocess.Popen(["aplay"],stdin=proc2.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE )
    stdout_value = proc3.communicate()[0]

def ecoute():
    print("Parler maintenant")
    audio=subprocess.Popen(["avconv","-f","alsa","-ac","2","-i","pulse","-acodec","flac","-y","tmp.flac","-b","16k"])
    import time
    time.sleep(5)
    audio.kill()
    """audio=subprocess.Popen(["arecord","-q","-f","cd","-t","wav","-d","5","-r","16000","text"],stdout=subprocess.PIPE)
    a=audio.communicate()[0]
    audio1=subprocess.Popen(["cat","text"],stdout=subprocess.PIPE)
    audio2=subprocess.Popen(["flac","--totally-silent","-","-f","--best","--sample-rate","16000","-o","tmp.flac"],stdin=audio1.stdout,stdout=subprocess.PIPE)
    b=audio2.communicate()[0]"""
    print("audio recup")
    trad=subprocess.Popen(["wget","-O","speech.txt","-U","Mozilla/5.0","--post-file","tmp.flac","--header=Content-Type:audio/x-flac;rate=16000","http://www.google.com/speech-api/v1/recognize?lang=fr&client=chromium"],stdout=subprocess.PIPE)
    t=trad.communicate()[0]
    print("trad recup")
    file=open('speech.txt','r')
    i=0
    for ligne in file:
        tmp = ligne
        i = i+1
    if i > 0:
        t=tmp.split(":")
        u=t[4].split(",")
        msg=u[0]
        msg=msg.replace("\"","")
    else:
        msg=""
    print("msg="+str(msg))
    return msg

#ecoute()
