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
    ip = "0.0.0.0"

    def __init__(self):
        """ Server launches, opens socket self.s waiting for users to connect """

        self.users = {}     # collect users (sockets)
        self.ips = {}       # collect ips from users

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
            self.ips[addr[0]] = "Connect"
            print("User joined room: " + str(addr) + " " + str(len(self.users)) + "/10")

            # send status info to user (who is in what room)
            user.send(str(self.ips).encode())

            threading.Thread(target=self.receive_audio_from_user, args=(user, addr,)).start()

    def receive_audio_from_user(self, user, addr):
        """ Receives from every user audio """

        while 1:

            try:

                # receive data
                data = user.recv(self.chunk_size)       # receive meessage from user conn
                string_data = data.decode('utf-8', "ignore")

                # channel switching message?
                if ("CLIENTMESSAGE" in string_data):

                    # find message
                    message_position_begin = string_data.find("CLIENTMESSAGE_")
                    message_position_end = string_data.find("_CLIENTMESSAGEEND")
                    message_content = string_data[message_position_begin+len("CLIENTMESSAGE_"):message_position_end]
                    full_message = string_data[message_position_begin:message_position_end+len("_CLIENTMESSAGEEND")]

                    # encode message
                    message_type = message_content.split("_")[0]   # room switch or something else?
                    message = message_content.split("_")[1]

                    # execute message
                    if (message_type == "roomswitch"):
                        print("User " + str(addr) + " switched to room: " + str(message))
                        self.users[user] = message                # update room
                        self.ips[addr[0]] = message                  # update room

                    string_data.replace(full_message, full_message + "_" + str(addr))
                    data = string_data.encode()

                    # print messages
                    print("Message content: " + str(message_content))
                    print("Full Message: " + str(full_message))
                    print("Message Type: " + str(message_type))

                # start sending data to everyone inclusive messages
                self.send_audio_to_users(user, data)

            except socket.error:

                # Error? Disconnect user
                print("User disconnected from Server!")
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
                    print("Error sending data to a user! " + str(selected_user))
                    break

server = Server()
