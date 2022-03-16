import pyaudio
import numpy as np
import threading
from statistics import mode

class LISTENER():
    def __init__(self):
        self.run = True
        self.hungUp = "hung up"
        self.waiting = "waiting for someone to pick up"
        self.recording = "recording"
        self.currentState = None

        # Audio variables
        CHUNK = 4096
        RATE = 44100
        power = 12

        self.p = pyaudio.PyAudio()
        # Opens audio stream
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        listenThread = threading.Thread(target=self.capture)
        listenThread.start()

    def getCurrentState(self):
        return self.currentState

    def capture(self):
        def sample():
            # Audio variables
            CHUNK = 4096
            #CHUNK = 1000
            RATE = 44100
            power = 12
            # Reads the data
            data = np.fromstring(self.stream.read(CHUNK), dtype=np.int16)

            # Calculates the peak of the frequency
            peak = np.average(np.abs(data)) * 2

            # Shows the bars for amplitude
            bars = "#" * int(50 * peak / 2 ** power)

            # Calculates the frequency from with the peak ws
            data = data * np.hanning(len(data))
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft) / 2)]
            freq = np.fft.fftfreq(CHUNK, 1.0 / RATE)
            freq = freq[:int(len(freq) / 2)]
            freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1

            # Shows the peak frequency and the bars for the amplitude
            #print("peak frequency: %d Hz" % freqPeak + " " + bars)
            return round(freqPeak), int(50 * peak / 2 ** power) #amps

        while self.run:
            sampleRate = 10
            sampleArray = []
            ampsArray = []
            for i in range(0, sampleRate):
                freq, amps = sample()
                sampleArray.append(freq)
                ampsArray.append(amps)
            commonFreq = mode(sampleArray)
            commonAmps = mode(ampsArray)
            #print("Freq:"+str(commonFreq))
            #print("Amps:"+str(commonAmps))
            if commonAmps == 0:
                self.currentState = self.hungUp
            elif commonFreq >= 19.0 and commonFreq <= 25:
                self.currentState = self.waiting
            else:
                self.currentState = self.recording

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("ended listening")



