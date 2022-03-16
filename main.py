from listener import LISTENER
import time
from tone import sinePlay
from pydub import AudioSegment
from pydub.playback import play
from recorder import recordObj
from tkinter import *
import threading
song = AudioSegment.from_wav("wedding_greeting.wav")

l = LISTENER()

tone = sinePlay()
while True: #run forever for now, this is our state machine
    #init state is waiting for someone to pick up
    #play the tone
    tone.start()
    time.sleep(2)
    while l.getCurrentState() == l.waiting:
        print(l.getCurrentState())
        time.sleep(1)
    print("Someone picked up")
    #someone has picked up the phone! play the greeting...
    tone.stop()
    play(song)

    #now record for a period of time
    r = recordObj()
    print(l.getCurrentState())
    while l.getCurrentState() != l.hungUp:
        print(l.getCurrentState())
        time.sleep(1)
    r.stopRecording()
    tone.start()
    print("START OVER")