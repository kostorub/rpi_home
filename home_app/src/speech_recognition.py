import json
import os

import pyaudio
from vosk import KaldiRecognizer, Model


class SpeechRecognition:
    def __init__(self, path):
        if not os.path.exists(path):
            print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
            exit (1)

        self.model = Model(path)
        self.rec = KaldiRecognizer(self.model, 16000)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()

    def recognition_loop(self, *args, **kwargs):
        data = self.stream.read(4000)
        if len(data) == 0:
            return
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())
            text = result.get("text")
            if not text:
                text = "Speak!"
            callback = kwargs.get("callback")
            if callback:
                callback(text)
