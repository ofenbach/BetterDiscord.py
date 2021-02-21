import threading

import ui
import client

def main():

    #threading.Thread(target=client.Client).start()
    #ui.UI()
    client.Client()

main()