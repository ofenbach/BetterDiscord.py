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
        users_room1_test = []
        users_room2_test = []
        users_room3_test = []
        users_connect_room = [k for k,v in users_online.items() if str(v) == "Connect"]     # convert user dict to acutal ip list
        users_room1 = [k for k, v in users_online.items() if str(v) == "room1"]           # convert user dict to acutal ip list
        for user in users_room1:
            user.replace("", "User")
            users_room1_test.append(user)
        users_room2 = [k for k, v in users_online.items() if str(v) == "room2"]           # convert user dict to acutal ip list
        for user in users_room2:
            user.replace("", "User")
            users_room2_test.append(user)

        users_room3 = [k for k, v in users_online.items() if str(v) == "room3"]           # convert user dict to acutal ip list
        for user in users_room3 :
            user.replace("", "User")
            users_room3_test.append(user)

        print(users_room1_test, users_room2_test, users_room3_test)
        eel.update_users_view(str(users_connect_room), users_room1_test, users_room2_test, users_room3_test)

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

        users_room1_test = []
        users_room2_test = []
        users_room3_test = []
        for user in users_room1:
            if (user == ''):
                user = "User"
            users_room1_test.append(user)
        for user in users_room2:
            if (user == ''):
                user = "User"
            users_room2_test.append(user)
        for user in users_room3 :
            if (user == ''):
                user = "User"
            users_room3_test.append(user)

        # append myself to the user list in this room
        if (room_name == "room1"):
            users_room1_test.append("Me")
        if (room_name == "room2"):
            users_room2_test.append("Me")
        if (room_name == "room3"):
            users_room3_test.append("Me")

        print(users_room1_test)
        print(users_room2_test)
        print(users_room3_test)
        eel.update_users_view(str(users_connect_room), str(users_room1_test), str(users_room2_test), str(users_room3_test))

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
