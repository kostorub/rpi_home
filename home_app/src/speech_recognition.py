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
        self.rec = KaldiRecognizer(self.model, 48000)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=48000)
        self.stream.start_stream()

        self.can_command = False

    def recognition_loop(self, *args, **kwargs):
        data = self.stream.read(48000)
        if len(data) == 0:
            return
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())
            text = result.get("text")
            if not text:
                text = "Speak!"
            
            callback_permission = kwargs.get("callback_permission")
            if callback_permission and not self.can_command:
                callback_permission(text)
                return

            callback_speech = kwargs.get("callback_speech")
            if callback_speech:
                callback_speech(text)
        else:
            print(self.rec.PartialResult())
