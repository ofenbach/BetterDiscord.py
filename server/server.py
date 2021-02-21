import channel
import threading

class Server:
    """ Server that creates two channels that users can connect too
    Channel 1 Port: 1024, Channel 2 Port: 1025
    It creates a thread for each channel
    """

    free_port = 1024         # main channel port

    def __init__(self):

        # channellist entries: (port, name)
        self.channels = []  # collect channel names

        # create channels
        self.create_channel("main")
        self.create_channel("side")

        # message
        print("Server created:")
        print("   Main Channel (0/10)")
        print("   Side Channel (0/10)")

    def create_channel(self, name):
        self.channels.append((name, Server.free_port))
        threading.Thread(target=channel.Channel, args=(name, Server.free_port,)).start()
        Server.free_port += 1
        print("Channel created: " + str(name))

    def delete_channel(self, name, port):
        """ Remove a channel from the list TODO: disconnect socket """
        self.channels.remove((name, port))
        print("Channel removed: " + name)

server = Server()