import wx
from loginFrame import loginFrame as Frame


class App(wx.App):
    def OnInit(self):
        self.frame = Frame(None)
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
