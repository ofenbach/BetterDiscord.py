#!/usr/bin/env python3

import sys
import socket
import threading

import pyaudio
import ast

class Client:

    def __init__(self):
        """ Sets default values """

        # settings
        self.current_room = "Connect"
        self.muted = False
        self.deaf = False
        self.SERVER_IP = '135.125.207.61'              # Alternatives: "hackinto.myftp.org" "127.0.0.1"
        self.PORT = 4848
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt32
        self.channels = 1
        self.rate = 48000

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        """ Client connects to server socket, starts two threads: sending and receiving audio """

        self.s.connect((self.SERVER_IP, self.PORT))    # connect to server

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate, output=True,frames_per_buffer=self.chunk_size)
        self.recording_stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

        # read server join message
        data = self.s.recv(1024)
        self.users = ast.literal_eval(data.decode('utf-8', "ignore"))

        print("[CONNECTED] " + self.SERVER_IP + ":" + str(self.PORT))

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        receive_thread = threading.Thread(target=self.send_data_to_server).start()

    def stop_client(self):
        """ TODO: Fixing real disconnect """
        self.s.close()
        print("[DISCONNECTED]")

    def receive_server_data(self):
        """ Start receiving audio data from the socket """

        while 1:
            try:

                data = self.s.recv(self.chunk_size)             # receive audio and play it if not deaf
                string_data = data.decode('utf-8', "ignore")

                if ("CLIENTMESSAGE" in string_data):            # channel switching message?
                    message_position_begin = string_data.find("CLIENTMESSAGE_")
                    message_position_end = string_data.find("_CLIENTMESSAGEEND")
                    message_content = string_data[message_position_begin+len("CLIENTMESSAGE_"):message_position_end]
                    full_message = string_data[message_position_begin:message_position_end+len("_CLIENTMESSAGEEND")]
                    ip_end = string_data.find("_IPEND")
                    ip_port = string_data[message_position_end+len("_CLIENTMESSAGEEND_"):ip_end]
                    message_type = message_content.split("_")[0]    # room switch or something else?
                    message = message_content.split("_")[1]

                    if (message_type == "roomswitch"):              # execute message
                        print("User switched to room: " + str(message) + str(ip_port))
                        self.users[ip_port] = message                                    # update room TODO: update ui

                if (not self.deaf and not self.current_room == "Connect"):
                    self.playing_stream.write(data)

            except Exception as e:
                self.s.close()
                print("[ERROR] Receiving Data" + str(e))
                sys.exit()

    def send_data_to_server(self):
        """ Send audio data to socket """

        while 1:
            try:
                data = self.recording_stream.read(self.chunk_size, exception_on_overflow = False)   # record audio and send it if not muted
                if (not self.muted) and (self.current_room != "Connect"):
                    self.s.sendall(data)

            except Exception as e:
                print("[ERROR] Sending Data" + str(e))
                sys.exit()

    def enter_room(self, name):
        """ Sends message to s socket with the room name
        Parameter: name of the new room """

        message = "CLIENTMESSAGE_roomswitch_" + str(name) + "_CLIENTMESSAGEEND"
        self.s.send(str(message).encode())
        self.current_room = str(name)
        print("[ROOMSWITCH] " + str(name))
