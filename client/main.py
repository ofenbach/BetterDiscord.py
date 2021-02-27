import wxui
import client
import ui

def main():
    """ Runs the UI which runs the client """

    #wxui.drawUI(client.Client())
    ui.startUI(client.Client())

main()