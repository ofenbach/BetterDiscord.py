__author__ = "Tim B. Ofenbach"
__copyright__ = "Copyright 2021"
__credits__ = ["l33tlinuxh4x0r"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Tim B. Ofenbach"
__email__ = "t.ofenbach@gmail.com"
__status__ = "Production"

import socket
import threading

class Server:
    """ Server that creates one socket that users can connect to.
    Users can switch rooms by sending a message to that socket starting with "room_"""

    # server access
    port = 4848
    #ip = '54.37.205.19'
    #ip = socket.gethostbyname(socket.gethostname())
    #print(ip)
    ip = "0.0.0.0"

    def __init__(self):
        """ Server launches, opens socket self.s waiting for users to connect """

        self.users = {}     # collect users

        # audio
        self.chunk_size = 1024    # TODO: Perfect combination quality vs. delay

        # setup socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((Server.ip, Server.port))
        self.s.listen()

        # listen if users connect
        while True:
            user, addr = self.s.accept()
            self.users[user] = "main"           # default room: main
            print("Dictionary: ")
            print(self.users)
            print("User joined room: " + str(addr) + " " + str(len(self.users)) + "/10")
            threading.Thread(target=self.receive_audio_from_user, args=(user, addr,)).start()

    def receive_audio_from_user(self, user, addr):
        """ Receives from every user audio """

        while 1:

            try:

                # receive data
                data = user.recv(self.chunk_size)       # receive audio from user conn
                string_data = data.decode('utf-8', "ignore")

                # channel switching message?
                if ("roomMSGCUT" in string_data):

                    # find room name
                    room_name = string_data.split("MSGCUT")[1]
                    print("User switched channel: " + str(addr) + "  to  " + room_name)
                    self.users[user] = room_name  # update channel

                    # remove message to not send it to everyone
                    string_data.replace("roomMSGCUT" + room_name + "MSGCUTend", "")
                    data = string_data.encode('utf-8', "ignore")

                    print("Dictionary: ")
                    print(self.users)

                # start sending audio to everyone
                self.send_audio_to_users(user, data)    # then send it to everyone else

            except socket.error:

                # Error? Disconnect user
                del self.users[user]
                print("User left room: "+ str(len(self.users)))    # slicing out rooms name
                user.close()
                break

    def send_audio_to_users(self, sock, data):
        """ Sends the audio received to every user """

        self.users_copy = self.users.copy() # copy to make sure no one joins while sending data

        # send audio to every user in channel
        for user in self.users_copy:
            if user != self.s and user != sock: #and self.users[user] == self.users[sock]:    # same channel and not himself and not server
                try:
                    user.send(data) # send audio to everyone in your channel
                except Exception as e:
                    print("Error sending data to a user! " + str(e))
                    break

server = Server()
