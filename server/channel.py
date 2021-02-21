import socket
import threading

class Channel:

    #ip = socket.gethostbyname(socket.gethostname())
    ip = '54.37.205.19'

    def __init__(self, name, port):
        """ Creates new channel with individual port """

        # define id
        self.name = name
        self.port = port

        # users
        self.users = []
        self.accept_user_joins()

        # audio
        self.chunk_size = 64

    def accept_user_joins(self):
        """ Always checks if user wants to connect """

        # setup socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((Channel.ip, self.port))
        self.s.listen()

        # listen if users connect
        while True:
            conn, addr = self.s.accept()
            self.users.append(conn)
            print("New User connected in channel " + self.name + ": " + str(len(self.users)) + "/10")
            threading.Thread(target=self.receive_audio_from_user, args=(conn, addr,)).start()

    def receive_audio_from_user(self, conn, addr):
        """ Receives from every user audio """

        while 1:
            try:
                data = conn.recv(self.chunk_size)       # receive audio from user conn
                self.send_audio_to_users(conn, data)    # then send it to everyone else
            except socket.error:
                self.users.remove(conn)
                print("User left channel: " + self.name +" "+ str(len(self.users)) + "/10") # TODO: Fix: Server crashes
                conn.close()    # TODO: Socket reconnect bugs
                break

    def send_audio_to_users(self, sock, data):
        """ Sends the audio received to every user """

        # go through ever user
        for user in self.users:
            if user != self.s and user != sock:
                try:
                    user.send(data) # send audio to everyone except yourself
                except:
                    print("Error sending data to user " + str(user))