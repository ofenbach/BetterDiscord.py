import wx

class UI:
    def __init__(self):
        app = wx.App()
        window = wx.Frame(None, size=(1080, 720))
#         panel = wx.Panel(window)
        
        window.SetTitle("Better Discord (dot) py")
        
        window.SetBackgroundColour("#030017")
        
        window.Show(True)
    
        app.MainLoop()
        
UI()