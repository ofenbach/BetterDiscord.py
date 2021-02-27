#!/usr/bin/env python3

import socket
import threading

import pyaudio

import wxui

class Client:

    def __init__(self):
        """ Sets default values """

        # default settings
        self.current_room = "Connect"
        self.muted = False
        self.deaf = False

        # server selection
        self.ip = '54.37.205.19'  # ip of tims server
        # self.ip = "hackinto.myftp.org"
        # self.ip = "127.0.0.1" #local ip for testing (as long as the server is on the same machine as the client)
        self.port = 4848  # default main room

        # Default Audio Settings
        self.chunk_size = 1024  # 1024
        self.audio_format = pyaudio.paInt32
        self.channels = 1
        self.rate = 48000  # 20000

        # create socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        """ Client connects to server socket,
                starts two threads: sending and receiving audio """

        # connect
        self.s.connect((self.ip, self.port))

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate, output=True,frames_per_buffer=self.chunk_size)
        self.recording_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

        # Success Message
        print("Connected to Server: " + self.ip + ":" + str(self.port))
        print("Room: " + str(self.current_room))

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        receive_thread = threading.Thread(target=self.send_data_to_server).start()

    def stop_client(self):
        """ TODO: Fixing real disconnect """
        self.s.close()
        print("Disconnected")

    def receive_server_data(self):
        """ Start receiving audio data from the socket """

        run_loop = True

        while run_loop:

            try:

                # receive audio and play it if not deaf
                data = self.s.recv(self.chunk_size)
                if (not self.deaf or not self.current_room == "Connect"):
                    self.playing_stream.write(data)

            except Exception as e:

                # Error? Disconnnect!
                self.s.close()
                run_loop = False
                print("Error while receiving server data: " + str(e))

    def send_data_to_server(self):
        """ Send audio data to socket """

        while True:
            try:

                # record audio and send it if not muted
                data = self.recording_stream.read(self.chunk_size, exception_on_overflow = False)
                if (not self.muted) and (self.current_room != "Connect"):
                    self.s.sendall(data)

            except Exception as e:

                # Error? Disconnect!
                self.s.close()
                print("Error while sending data to server: " + str(e))

    def enter_room(self, name):
        """ Sends message to s2 socket with the room name
        Parameter: name of the new room """
        message = "roomMSGCUT" + str(name) + "MSGCUTend"
        print("Room switched: " + str(name))
        self.s.send(str(message).encode())
        self.current_room = str(name)
