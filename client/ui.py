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
        client.start_client()
    @eel.expose
    def enter_room(room_name):
        client.enter_room(room_name)
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

