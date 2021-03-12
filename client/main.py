import client
import ui

def main():
    """ Runs the UI which runs the client """
    try:
        client_ = client.Client()
        ui.startUI(client_)
    finally:
        client_.stop_client()

main()