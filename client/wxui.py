import os
import wx
from wx.svg import SVGimage

class UI:

    def drawUI(self):
        
        def OnClicked(event):
            pass

        # room switch event
        def OnRooms(event):
            if rooms.GetStringSelection() == "Lobby":
                print("room switched: main")      # set room main
                self.connect_room(1024)
            elif rooms.GetStringSelection() == "Room 1":
                print("room switched: Room 1")
                self.connect_room(1025)
            elif rooms.GetStringSelection() == "Secret room":
                print("room switched: Secret room")
                self.connect_room(1337)
            elif rooms.GetStringSelection() == "Null":
                print("room switched: Null")
                self.connect_room(6969)

        # options events
        def OnMute(event):
            self.muted = not self.muted
            print("muted " + str(self.muted))
        def OnDeaf(event):
            self.deaf = not self.deaf
            print("deaf " + str(self.deaf))
        def OnLeave(event):
            window.Close()
        
        # window stuff
        resolution = (1080, 720)
        icon_size = wx.Size(16, 16)
        bsize = (32, 32)
        app = wx.App()

        # sets the default window size
        window = wx.Frame(None, size=resolution)
        # makes the window so that it can't be shrunk less than the default size
        window.SetMinSize(resolution)

        # settings for window
        window.SetBackgroundColour("#030017")
        window.SetTitle("Better Discord (dot) py")

        # make panels left, middle and right and set attributes
        panel = wx.Panel(window)
        left_panel = wx.Panel(panel, size=(200, wx.EXPAND))
        left_panel.SetBackgroundColour("#251C3B")
        left_panel.SetForegroundColour("white")

#         # for future expansion
#         mid_panel = wx.Panel(panel)
#         right_panel = wx.Panel(panel)

        # load images
        img_deaf = SVGimage.CreateFromFile("graphics/ear_deaf.svg")
        img_undeaf = SVGimage.CreateFromFile("graphics/ear_undeaf.svg")
        img_leave = SVGimage.CreateFromFile("graphics/leave_room.svg")
        img_mic = SVGimage.CreateFromFile("graphics/mic.svg")
        img_muted = SVGimage.CreateFromFile("graphics/mic_muted.svg")
        img_rnnoise = SVGimage.CreateFromFile("graphics/noise_suppression.svg")
        img_rnnoised = SVGimage.CreateFromFile("graphics/noise_suppressed.svg")
        img_room = SVGimage.CreateFromFile("graphics/room.svg")
        img_settings = SVGimage.CreateFromFile("graphics/settings.svg")

        # convert images to a usable format
        bmp_deaf = img_deaf.ConvertToScaledBitmap(icon_size)
        bmp_undeaf = img_undeaf.ConvertToScaledBitmap(icon_size)
        bmp_leave = img_leave.ConvertToScaledBitmap(icon_size)
        bmp_mic = img_mic.ConvertToScaledBitmap(icon_size)
        bmp_muted = img_muted.ConvertToScaledBitmap(icon_size)
        bmp_rnnoise = img_rnnoise.ConvertToScaledBitmap(icon_size)
        bmp_rnnoised = img_rnnoised.ConvertToScaledBitmap(icon_size)
        bmp_room = img_room.ConvertToScaledBitmap(icon_size)
        bmp_settings = img_settings.ConvertToScaledBitmap(icon_size)

        # rooms header
        rooms_text = wx.StaticText(panel, label="Rooms", size=(200, 20), style=wx.ALIGN_CENTER)
        rooms_text.SetForegroundColour("white")

        # replaced with listbox!
        room_list = ["Lobby", "Room 1", "Secret room", "Null"]
        rooms = wx.ListBox(left_panel, size=(190, 360), choices=room_list, style=wx.LB_SINGLE)
        #rooms.SetBackgroundColour("#251C3B")
        #rooms.SetItemBackgroundColour("white")
        app.Bind(wx.EVT_LISTBOX, OnRooms, rooms)
        
        # add actions bar
        settings_b = wx.Button(left_panel, size=bsize)
        settings_b.SetBitmap(bmp_settings)
        settings_b.Bind(wx.EVT_BUTTON, OnClicked)
        
        mute_b = wx.ToggleButton(left_panel, size=bsize)
        mute_b.SetBitmap(bmp_mic)
        mute_b.SetBitmapPressed(bmp_muted)
        mute_b.Bind(wx.EVT_BUTTON, OnMute)
        
        deaf_b = wx.ToggleButton(left_panel, size=bsize)
        deaf_b.SetBitmap(bmp_deaf)
        deaf_b.SetBitmapPressed(bmp_undeaf)
        deaf_b.Bind(wx.EVT_BUTTON, OnDeaf)

        rnnoise_b = wx.ToggleButton(left_panel, size=bsize)
        rnnoise_b.SetBitmap(bmp_rnnoise)
        rnnoise_b.SetBitmapPressed(bmp_rnnoised)
        rnnoise_b.Bind(wx.EVT_BUTTON, OnClicked)

        leave_b = wx.Button(left_panel, size=bsize)
        leave_b.SetBitmap(bmp_leave)
        leave_b.Bind(wx.EVT_BUTTON, OnLeave)

        # main panels controlled by sizers h/v and left, mid and right
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        l_sizer = wx.BoxSizer(wx.VERTICAL)

#         # for future additions...
#         m_sizer = wx.BoxSizer(wx.VERTICAL)
#         r_sizer = wx.BoxSizer(wx.VERTICAL)

        # sizer for rooms

        # adding items to sizer
        l_sizer.AddSpacer(10)
        l_sizer.Add(rooms_text)
        l_sizer.AddSpacer(10)
        l_sizer.Add(rooms, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # sizer for action buttons
        action_sizer = wx.BoxSizer(wx.HORIZONTAL)
        action_sizer.AddStretchSpacer()
        action_sizer.Add(settings_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(mute_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(deaf_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(rnnoise_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(leave_b)
        
        action_sizer.AddStretchSpacer()

        l_sizer.AddStretchSpacer()      
        l_sizer.Add(action_sizer, flag=wx.EXPAND)

        main_sizer.Add(l_sizer, flag=wx.EXPAND)

        panel.SetSizer(main_sizer)

        # show everything :P
        window.Show()
        app.MainLoop()