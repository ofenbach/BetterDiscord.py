import channel
import threading

class Server:

    ip = '54.37.205.19'
    free_port = 1024         # main channel port = 1024

    def __init__(self):

        # channels
        self.channels = []  # collect channel names

        # create main channel
        self.create_channel("main")
        self.create_channel("side")
        print("Server created:")
        print("   Main Channel (0/10")
        print("   Side Channel (0/10")

    def create_channel(self, name):
        self.channels.append((name, Server.free_port))
        threading.Thread(target=channel.Channel, args=(name, Server.free_port,)).start()
        #main_channel = channel.Channel(name, Server.free_port)
        Server.free_port += 1
        print("Channel created: " + str(name))

    def delete_channel(self, name, port):
        self.channels.remove((name, port))
        print("Channel removed: " + name)

server = Server()