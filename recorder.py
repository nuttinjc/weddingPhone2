import pyaudio
import wave
import time
import threading
import datetime

class recordObj():
    def __init__(self):
        # set the chunk size of 1024 samples
        self.chunk = 1024
        # sample format
        self.FORMAT = pyaudio.paInt16
        # mono, change to 2 if you want stereo
        self.channels = 1
        # 44100 samples per second
        self.sample_rate = 44100
        self.record_seconds = 1
        # initialize PyAudio object
        self.p = pyaudio.PyAudio()
        # open stream object as input & output
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)
        self.frames = []
        self.keepRecording = True
        self.startRecord()

    def startRecord(self):
        def record():
            while self.keepRecording:
                for i in range(int(self.sample_rate / self.chunk * self.record_seconds)):
                    data = self.stream.read(self.chunk)
                    # if you want to hear your voice while recording
                    # stream.write(data)
                    self.frames.append(data)
        print("recording")
        recordThread = threading.Thread(target=record)
        recordThread.start()

    def stopRecording(self):
        print("stop recording")
        self.keepRecording = False
        time.sleep(1)
        self.stream.stop_stream()
        self.stream.close()
        # terminate pyaudio object
        self.p.terminate()
        # save audio file
        # open the file in 'write bytes' mode
        fileName = datetime.datetime.now()
        date, curr_time = str(fileName).split(" ")
        curr_time = str(curr_time).replace(":", "-")
        fileName = str(date)+curr_time
        fileName = fileName +".wav"
        fileName = r"C:\Users\justi\pythonProject\weddingPhone2\recordings\\"+fileName
        wf = wave.open(fileName, "wb")
        # set the channels
        wf.setnchannels(self.channels)
        # set the sample format
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        # set the sample rate
        wf.setframerate(self.sample_rate)
        # write the frames as bytes
        wf.writeframes(b"".join(self.frames))
        # close the file
        wf.close()