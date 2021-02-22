#!/usr/bin/env python3

import socket

import pyaudio
import threading
from tkinter import *
from tkinter import ttk

from wxui import UI

class Client:

    def __init__(self):

        # server selection
        self.ip = '54.37.205.19'
        #self.ip = '192.168.2.56'
        self.port = 1024        # default main channel

        # Default Audio Settings
        self.chunk_size = 64  # 1024
        self.audio_format = pyaudio.paInt32
        self.channels = 1
        self.rate = 48000  # 20000

        # Client Settings
        self.muted = False
        self.deaf = False

        self.connect_channel(self.port)
        self.render_ui()

    def connect_channel(self, port):
        # create socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect
        self.s.connect((self.ip, self.port))

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate, output=True,frames_per_buffer=self.chunk_size)
        self.recording_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

        # Success Message
        print("Connected to Server: " + self.ip)

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        receive_thread = threading.Thread(target=self.send_data_to_server).start()

    def receive_server_data(self):
        print("Headphones are getting audio")
        while True:
            try:
                data = self.s.recv(self.chunk_size)
                if (not self.deaf):
                    self.playing_stream.write(data) # TODO: if deaf dont
            except:
                print("Error while receiving server data!")

    def send_data_to_server(self):
        print("Microphone is sending audio")
        while True:
            try:
                data = self.recording_stream.read(self.chunk_size, exception_on_overflow = False)
                if (not self.muted):
                    self.s.sendall(data)
            except Exception as e:
                print("Error while sending data to server!")
                print(e)


    def render_ui(self):
       UI.drawUI(self)
        