import socket
import wave
import pyaudio

class MusicBot:
    """ Start it and it will join room 1 """

    def __init__(self):

        # songs
        self.song1 = wave.open('song.wav', 'rb')
        self.p = pyaudio.PyAudio()
        self.song1_stream = self.p.open(format=self.p.get_format_from_width(self.song1.getsampwidth()), channels=self.song1.getnchannels(),
                        rate=self.song1.getframerate(),
                        output=True)
        self.song2 = wave.open('song2.wav', 'rb')
        self.song2_stream = self.p.open(format=self.p.get_format_from_width(self.song2.getsampwidth()),
                                        channels=self.song2.getnchannels(),
                                        rate=self.song2.getframerate(),
                                        output=True)
        self.song3 = wave.open('song3.wav', 'rb')
        self.song3_stream = self.p.open(format=self.p.get_format_from_width(self.song3.getsampwidth()),
                                       channels=self.song3.getnchannels(),
                                      rate=self.song3.getframerate(),
                                     output=True)
        self.song3 = ""
        self.songs = [self.song1, self.song2, self.song3]
        self.song_counter = 0

        # connecting
        self.ip = '54.37.205.19'
        self.port = 4848
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, self.port))
            print("Connected to " + self.ip)
        except:
            print("Error connecting")

        # room switch
        message = "CLIENTMESSAGE_roomswitch_" + "room1" + "_CLIENTMESSAGEEND"
        self.s.send(str(message).encode())

        while True:
            # read data (based on the chunk size)
            data = self.songs[self.song_counter].readframes(1024)

            while data != '':
                self.s.sendall(data)
                data = self.songs[self.song_counter].readframes(1024)

            self.song_counter += 1

MusicBot()
