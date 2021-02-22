import room
import threading

class Server:
    """ Server that creates two rooms that users can connect too
    Room 1 Port: 1024, Room 2 Port: 1025
    It creates a thread for each room
    TODO: Is it better to use one main socket and everyone connects to that or use a socket for each room? @l33tlinux
    """

    free_port = 1024         # main room port

    def __init__(self):

        # roomlist entries: (port, name)
        self.rooms = []  # collect room names

        # create rooms
        self.create_room("main")
        self.create_room("side")

        # message
        print("Server created:")
        print("   Main room (0/10)")
        print("   Side room (0/10)")

    def create_room(self, name):
        self.rooms.append((name, Server.free_port))
        threading.Thread(target=room.Room, args=(name, Server.free_port,)).start()
        Server.free_port += 1
        print("room created: " + str(name))

    def delete_room(self, name, port):
        """ Remove a room from the list TODO: disconnect socket """
        self.rooms.remove((name, port))
        print("room removed: " + name)

server = Server()