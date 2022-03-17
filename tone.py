from pysine import sine
import threading

class sinePlay():
    def __init__(self):
        self.play = False
        listenThread = threading.Thread(target=self.listen)
        listenThread.start()

    def listen(self):
        while True:
            if self.play:
                self.playTone()

    def playTone(self):
        sine(frequency=20, duration=.5)

    def stop(self):
        self.play = False

    def start(self):
        self.play = True