import json
import os
import asyncio

import pyaudio
from vosk import KaldiRecognizer, Model
from asyncio import sleep
from threading import Timer



class SpeechRecognition:
    def __init__(self, path, config, relays, loop=None):
        if not os.path.exists(path):
            print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
            exit (1)

        self.chunk = 1024 * 48

        self.model = Model(path)
        self.rec = KaldiRecognizer(self.model, self.chunk)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=self.chunk)
        self.stream.start_stream()

        self.can_command = False

        self.config = config
        self.relays = relays

        self.loop = loop or asyncio.get_event_loop()

        self.loop.create_task(self.recognition_loop())



    async def recognition_loop(self, *args, **kwargs):
        while True:
            data = self.stream.read(self.chunk, False)
            if len(data) == 0:
                return
            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get("text")
                print(text)
                if not text:
                    text = "Speak!"
                
                if self.check_call_sign(text) and not self.can_command:
                    self.allow_command()
                    continue
                
                if self.can_command:
                    self.on_speech(text)
            else:
                print(self.rec.PartialResult())
            
            await sleep(0.2)

    def on_speech(self, text):
        relay, state = self.relays.find_similar_phrase(text)
        if relay:
            relay.on() if state else relay.off()

    def check_call_sign(self, text):
        if text == self.config["call_sign"]:
            return True

    def allow_command(self):
        self.can_command = True
        self.timer = Timer(30, self.deny_command)
        self.timer.start()

    def deny_command(self):
        self.can_command = False