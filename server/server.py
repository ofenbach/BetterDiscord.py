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

            # wait for joins
            user, addr = self.s.accept()

            # user joined
            self.users[user] = "Connect"           # default room: Connect
            print("User joined room: " + str(addr) + " " + str(len(self.users)) + "/10")

            # send status info to user TODO: Bug: when user leaves count doesnt decrease
            self.online_users = str(len(self.users))
            user.send(self.online_users.encode())

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
                del self.users[user]
                break

    def send_audio_to_users(self, speaking_user, data):
        """ Sends the audio received to every user
        Params: socket is the user speaking , data the collected audio from the user speaking """

        # copy current connected users to make sure no one joins while sending data
        self.users_copy = self.users.copy()

        # check every user in server
        for selected_user in self.users_copy:

            # I   check so the speaking user is not sending it to the server
            # II  check so the speaking user is not sending it to himself
            # III check so the speaking user is in the same room as the current selected user
            if selected_user != self.s and selected_user != speaking_user and self.users[selected_user] == self.users[speaking_user]:
                try:
                    selected_user.send(data)     # send audio to selected user then for loop chooses next user
                except Exception as e:
                    print("Error sending data to a user! " + str(e))
                    break

server = Server()
