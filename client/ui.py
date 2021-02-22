from tkinter import *

class UI:

    def __init__(self):
        # window start
        window = Tk()
        window.geometry('1080x720')
        window.configure(background='#030017')

        # titel
        window.title("Voice Chat 1.0")

        # left: room overview
        room = Label(window, text="Lounges", bg='#261C3B', fg = 'white', font=("Arial Bold", 30), width=10, height=2)
        room.grid(column=0, row=0)

        # room main button
        def OnPressed(event):
            print('room switched: main')      # set room main
            self.connect_room(1024)
        def OnHover(event):
            main_btn.config(bg='#372957', fg='white')
        def OnLeave(event):
            main_btn.config(bg='#261C3B', fg='white')
        main_btn = Label(window, text='Main',fg='white', bg='#261C3B', font=("Arial Bold", 20), width=15, height=5)
        main_btn.bind('<Button-1>', OnPressed)
        main_btn.bind('<Enter>', OnHover)
        main_btn.bind('<Leave>', OnLeave)
        main_btn.grid(column=0, row=1)

        # room side button
        def OnPressed2(event):
            print('room switched: side')      # set room main
            self.connect_room(1025)
        def OnHover2(event):
            side_btn.config(bg='#372957', fg='white')
        def OnLeave2(event):
            side_btn.config(bg='#261C3B', fg='white')
        side_btn = Label(window, text='Side', fg='white', bg='#261C3B', font=("Arial Bold", 20), width=15, height=5)
        side_btn.bind('<Button-1>', OnPressed2)
        side_btn.bind('<Enter>', OnHover2)
        side_btn.bind('<Leave>', OnLeave2)
        side_btn.grid(column=0, row=2)

        # bottom: options label
        options = Label(window, text="Options: ", font=("Arial Bold", 30))
        options.grid(column=0, row=3)

        # mute button
        def OnPressed3(event):
            self.muted = not self.muted
            print("muted " + str(self.muted))  # set room main
            if (self.muted):
                photo = PhotoImage(file="microphone_muted.png")
                mute_btn.config(image=photo)
            else:
                photo = PhotoImage(file="microphone.png")
                mute_btn.config(image = photo)
        def OnHover3(event):
            mute_btn.config(bg='#372957', fg='white')
        def OnLeave3(event):
            mute_btn.config(bg='#261C3B', fg='white')

        photo = PhotoImage(file="microphone.png")
        mute_btn = Label(window, text='mute', image = photo, fg='white', bg='#261C3B', font=("Arial Bold", 20), width=50, height=60)
        mute_btn.bind('<Button-1>', OnPressed3)
        mute_btn.bind('<Enter>', OnHover3)
        mute_btn.bind('<Leave>', OnLeave3)
        mute_btn.grid(column=1, row=3)

        # deaf button
        def OnPressed4(event):
            self.deaf = not self.deaf
            print("deaf " + str(self.deaf))  # set room main

        def OnHover4(event):
            deaf_btn.config(bg='#372957', fg='white')

        def OnLeave4(event):
            deaf_btn.config(bg='#261C3B', fg='white')

        deaf_btn = Label(window, text='deaf', fg='white', bg='#261C3B', font=("Arial Bold", 20), width=10, height=3)
        deaf_btn.bind('<Button-1>', OnPressed4)
        deaf_btn.bind('<Enter>', OnHover4)
        deaf_btn.bind('<Leave>', OnLeave4)
        deaf_btn.grid(column=2, row=3)

        window.mainloop()

#client = Client()
