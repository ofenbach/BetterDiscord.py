import eel

def startUI(client):
    """ NEW HTML BASED UI
    Parameter: client object """

    eel.init('ui')
    eel.start('index.html', block=False)

    # BEGIN UI

    # left room selection
    @eel.expose
    def connect_button_pressed():

        # connect to server
        client.start_client()

        # display every room
        eel.display_rooms()

        # get users online
        users_online = client.users

        # what user is in what room
        users_connect_room = [k for k,v in users_online.items() if str(v) == "Connect"]     # convert user dict to acutal ip list
        users_room1 = [k for k, v in users_online.items() if str(v) == "room1"]           # convert user dict to acutal ip list
        users_room2 = [k for k, v in users_online.items() if str(v) == "room2"]           # convert user dict to acutal ip list
        users_room3 = [k for k, v in users_online.items() if str(v) == "room3"]           # convert user dict to acutal ip list
        eel.update_users_view(len(str(users_connect_room)), users_room1, users_room2, users_room3)

    @eel.expose
    def enter_room(room_name):
        client.enter_room(room_name)
        eel.update_room_hover(room_name)

        # get users
        users_online = client.users

        # what user is in what room
        users_connect_room = [k for k, v in users_online.items() if str(v) == "Connect"]  # convert user dict to acutal ip list
        users_room1 = [k for k, v in users_online.items() if str(v) == "room1"]  # convert user dict to acutal ip list
        users_room2 = [k for k, v in users_online.items() if str(v) == "room2"]  # convert user dict to acutal ip list
        users_room3 = [k for k, v in users_online.items() if str(v) == "room3"]  # convert user dict to acutal ip list

        # append myself to the user list in this room
        if (room_name == "room1"):
            users_room1.append("Me")
        if (room_name == "room2"):
            users_room2.append("Me")
        if (room_name == "room3"):
            users_room3.append("Me")

        eel.update_users_view(len(str(users_connect_room)), users_room1, users_room2, users_room3)

        print(users_room1)
        print(users_room2)
        print(users_room3)

    @eel.expose
    def close_program():
        client.stop_client()

    # options buttons
    @eel.expose
    def mute_button_pressed():
        client.muted = not client.muted
        print("User mute: " + str(client.muted))
    @eel.expose
    def deaf_button_pressed():
        client.deaf = not client.deaf
        print("User deaf: " + str(client.deaf))

    # END UI




    while True:
        eel.sleep(10)

