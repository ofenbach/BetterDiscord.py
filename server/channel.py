import socket
import threading

class Channel:

    #ip = socket.gethostbyname(socket.gethostname())
    ip = '54.37.205.19'

    def __init__(self, name, port):
        """ Creates new channel with individual port """
        print(Channel.ip)
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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((Channel.ip, self.port))
        self.s.listen()

        while True:
            conn, addr = self.s.accept()
            self.users.append(conn)
            print("New User connected in channel " + self.name + ": " + str(len(self.users)) + "/10")
            threading.Thread(target=self.receive_audio_from_user, args=(conn, addr,)).start()

    def receive_audio_from_user(self, conn, addr):
        """ Receives from every user audio """
        while 1:
            try:
                data = conn.recv(self.chunk_size)
                self.send_audio_to_users(conn, data)
            except socket.error:
                self.users.remove(conn)
                print("User left channel: " + self.name +" "+ str(len(self.users)) + "/10") # TODO: Fix: Server crashes
                conn.close()
                break

    def send_audio_to_users(self, sock, data):
        """ Sends the audio received to every user """
        for user in self.users:
            if user != self.s and user != sock:
                try:
                    user.send(data)
                except:
                    print("Error sending data to user " + str(user))






    def user_leave(self, conn):
        self.users.remove(conn)

    def get_port(self):
        return self.port