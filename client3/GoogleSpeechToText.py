import pyaudio
import wave
import audioop
from collections import deque 
import os
import urllib.request
from ctypes import *
import re

import Client

def py_error_handler(filename, line, function, err, fmt):
    pass

def listen_for_speech():
    """
    Does speech recognition using Google's speech  recognition service.
    Records sound from microphone until silence is found and save it as WAV and then converts it to FLAC. Finally, the file is sent to Google and the result is returned.
    """
    #config
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    THRESHOLD = 180 #The threshold intensity that defines silence signal (lower than).
    SILENCE_LIMIT = 3 #Silence limit in seconds. The max ammount of seconds where only silence is recorded. When this time passes the recording finishes and the file is delivered.
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('/usr/lib32/libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
    #open stream
    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)

    #print("* listening. CTRL+C to finish.")
    all_m = []
    data = ''
    SILENCE_LIMIT = 3
    rel = int(RATE/chunk)
    slid_win = deque(maxlen=SILENCE_LIMIT*rel)
    started = False

    while (True):
        data = stream.read(chunk)
        slid_win.append (abs(audioop.avg(data, 2)))

        if(True in [ x>THRESHOLD for x in slid_win]):
            if(not started):
                print("starting record")
            started = True
            all_m.append(data)
        elif (started==True):
            print("finished")
            #the limit was reached, finish capture and deliver
            filename = save_speech(all_m,p)
            stt_google_wav(filename)
            #reset all
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT*rel)
            all_m= []
            print("listening ...")

    #print("* done recording")
    stream.close()
    p.terminate()


def save_speech(data, p):
    filename = 'output'
    # write data to WAVE file
    data = ''.encode('utf-8').join(data)
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(data)
    wf.close()
    return filename


def stt_google_wav(filename):
    #Convert to flac
    FLAC_CONV = 'flac -s -f '
    os.system(FLAC_CONV+filename+'.wav')
    f = open(filename+'.flac','rb')
    flac_cont = f.read()
    f.close()

    #post it
    lang_code='fr-FR'
    googl_speech_url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=%s&maxresults=6'%(lang_code)
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",'Content-type': 'audio/x-flac; rate=16000'}
    req = urllib.request.Request(googl_speech_url, data=flac_cont, headers=hrs)
    p = urllib.request.urlopen(req)
    rep=""
    try:
        res = eval(p.read())['hypotheses']
        rep=res[0]
        rep=rep.get('utterance')
    except:
        rep="pas compris"
    if rep=="":
        rep="pas compris"
    os.remove("output.wav")
    os.remove("output.flac")
    print("rep="+str(rep))
    if re.search("lulu",str(rep)):
        Client.sendMsg("T",rep)
    return "ok"

def run():
    listen_for_speech()    

def run_thread():
    import threading
    t=threading.Thread(None, run, None)
    t.start()
"""import Proxy
Proxy.connectProxy('https')
run()"""
