import socket
import threading

##############   INFO   ##############
__author__     =    "Tim B. Ofenbach"
__copyright__  =    "Copyright 2021"
__credits__    =    ["l33tlinuxh4x0r"]
__license__    =    ""
__version__    =    "0.1.0"
__maintainer__ =    "Tim B. Ofenbach"
__email__      =    "t.ofenbach@gmail.com"
__status__     =    "Production"
######################################

class Server:
    """ Server that creates one socket that users can connect to
        Manages rooms (who to send audio to) and client messages """

    # server access
    port = 4848
    ip = "0.0.0.0"

    def __init__(self):
        """ Server launches, opens socket self.s waiting for users to connect
            When someone connects, it starts a thread for handling this user """

        # setup
        self.users = {}                                             # collect users (sockets)
        self.ips = {}                                               # collect ips from users ("ip:port": room)
        self.chunk_size = 1024                                      # TODO: Perfect combination quality vs. delay
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # start socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((Server.ip, Server.port))
        self.s.listen()
        print("[SOCKET] Listening ...")

        while True:

            user, addr = self.s.accept()            # wait for joins

            # user joined
            self.users[user] = "Connect"            # default room: Connect
            ip_port = str(addr[0]) + ":" + str(addr[1])
            self.ips[ip_port] = "Connect"
            print("[CONNECT] " + str(ip_port))
            print("[USERS] " + str(self.ips))

            user.send(str(self.ips).encode())       # send status info to user (who is in what room)
            threading.Thread(target=self.receive_audio_from_user, args=(user, addr,)).start()

    def receive_audio_from_user(self, user, addr):
        """ Receives audio from every user then sends it to everyone in the same room """

        while 1:
            try:

                data = user.recv(self.chunk_size)       # receive data from user conn
                string_data = data.decode('utf-8', "ignore")

                if ("CLIENTMESSAGE" in string_data):    # channel switching message?
                    message_position_begin = string_data.find("CLIENTMESSAGE_")     # find message in data string
                    message_position_end = string_data.find("_CLIENTMESSAGEEND")
                    message_content = string_data[message_position_begin+len("CLIENTMESSAGE_"):message_position_end]
                    full_message = string_data[message_position_begin:message_position_end+len("_CLIENTMESSAGEEND")]
                    message_type = message_content.split("_")[0]    # find message type: e.g. roomswitch
                    message = message_content.split("_")[1]         # actual content

                    if (message_type == "roomswitch"):              # execute message
                        ip_port = str(addr[0]) + ":" + str(addr[1])
                        self.ips[ip_port] = message
                        self.users[user] = message
                        print("[ROOMSWITCH] " + str(ip_port) + " to " + str(message))

                    if (message_type == "disconnect"):              # execute message
                        ip_port = str(addr[0]) + ":" + str(addr[1])
                        del self.ips[ip_port]
                        del self.users[user]
                        print("[DISCONNECT] " + str(ip_port))

                    print("[STATUS] " + str(self.ips))

                    message_data = (str(full_message) + "_" + str(ip_port) + "_IPEND").encode()   # append IP to message
                    string_data.replace(full_message, "")                       # remove message from audio
                    data = string_data.encode()

                self.send_audio_to_users(user, data)    # start sending data to everyone inclusive messages
                self.send_message_to_users(user, message_data)

            except socket.error:

                # Error? Disconnect user TODO: remove IP from self.ips
                print("[DISCONNECT] " + str(user))
                print("TODO: Remove IP+Port out of self.ips ")
                user.close()
                del self.users[user]
                break

    def send_audio_to_users(self, speaking_user, data):
        """ Sends the audio received to every user
        Params: socket is the user speaking , data the collected audio from the user speaking """

        self.users_copy = self.users.copy()     # copy current connected users to make sure no one joins while sending data

        for selected_user in self.users_copy:   # check every user in server TODO: Improve performance, not check every user

            # I   check so the speaking user is not sending it to the server
            # II  check so the speaking user is not sending it to himself
            # III check so the speaking user is in the same room as the current selected user
            if selected_user != self.s and selected_user != speaking_user and self.users[selected_user] == self.users[speaking_user]:
                try:
                    selected_user.send(data)     # send audio to selected user then for loop chooses next user
                except Exception as e:
                    print("[ERROR] sending to: " + str(selected_user))
                    selected_user.close()
                    del self.users[selected_user]
                    break

    def send_message_to_users(self, speaking_user, message):
        """ Sends the messaged received to every user
        Params: message data """

        self.users_copy = self.users.copy()     # copy current connected users to make sure no one joins while sending data

        for user in self.users_copy:            # check every user in server
            if user != self.s and user != speaking_user:
                try:
                    user.send(message)          # send message to every user
                except Exception as e:
                    print("[ERROR] sending to: " + str(user))
                    user.close()
                    del self.users[user]
                    break

server = Server()
