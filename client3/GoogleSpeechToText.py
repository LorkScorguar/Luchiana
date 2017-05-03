"""
Module pour la gestion du STT et TTS
"""
import wave
from collections import deque
import os
import urllib.request
from ctypes import c_char_p, c_int, CFUNCTYPE, cdll
import re
import threading
import pyaudio
import audioop

import Client

def py_error_handler(filename, line, function, err, fmt):
    """Gestion des erreurs"""
    pass

def listen_for_speech():
    """
    Does speech recognition using Google's speech  recognition service.
    Records sound from microphone until silence is found and save it as WAV and
    then converts it to FLAC. Finally, the file is sent to Google and the
    result is returned.
    """
    #config
    chunk = 1024
    rate = 16000
    threshold = 180 #The threshold intensity that defines silence signal
    silence_limit = 3 #Silence limit in seconds which stop the recording
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int,
                                   c_char_p, c_int, c_char_p)

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('/usr/lib32/libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
    #open stream
    pya = pyaudio.PyAudio()

    stream = pya.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=rate,
                      input=True,
                      frames_per_buffer=chunk)

    #print("* listening. CTRL+C to finish.")
    all_m = []
    data = ''
    rel = int(rate/chunk)
    slid_win = deque(maxlen=silence_limit*rel)
    started = False

    while True:
        data = stream.read(chunk)
        slid_win.append(abs(audioop.avg(data, 2)))

        if True in [x > threshold for x in slid_win]:
            if not started:
                print("starting record")
            started = True
            all_m.append(data)
        elif started:
            print("finished")
            #the limit was reached, finish capture and deliver
            filename = save_speech(all_m, pya)
            stt_google_wav(filename)
            #reset all
            started = False
            slid_win = deque(maxlen=silence_limit*rel)
            all_m = []
            print("listening ...")

    #print("* done recording")
    stream.close()
    pya.terminate()


def save_speech(data, pya):
    """Ecrit l'uadio dans un fichier wav"""
    filename = 'output'
    # write data to WAVE file
    data = ''.encode('utf-8').join(data)
    wf = wave.open(filename+'.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pya.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(data)
    wf.close()
    return filename


def stt_google_wav(filename):
    """stt via google speech-api"""
    #Convert to flac
    FLAC_CONV = 'flac -s -f '
    os.system(FLAC_CONV+filename+'.wav')
    fichier = open(filename+'.flac', 'rb')
    flac_cont = fichier.read()
    fichier.close()

    #post it
    lang_code = 'fr-FR'
    googl_speech_url = "https://www.google.com/speech-api/"\
    "v1/recognize?xjerr=1&client=chromium"\
    "&pfilter=2&lang=%s&maxresults=6" % (lang_code)

    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7"
                         "(KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",
           'Content-type': 'audio/x-flac; rate=16000'}
    req = urllib.request.Request(googl_speech_url, data=flac_cont, headers=hrs)
    resp = urllib.request.urlopen(req)
    rep = ""
    try:
        res = eval(resp.read())['hypotheses']
        rep = res[0]
        rep = rep.get('utterance')
    except:
        rep = "pas compris"
    if rep == "":
        rep = "pas compris"
    os.remove("output.wav")
    os.remove("output.flac")
    print("rep="+str(rep))
    if re.search("lulu", str(rep)):
        Client.sendMsg("T", rep)
    return "ok"

def run():
    """Fonction de test"""
    listen_for_speech()

def run_thread():
    """Lancement dans un thread"""
    thread = threading.Thread(None, run, None)
    thread.start()
#import Proxy
#Proxy.connectProxy('https')
#run()
