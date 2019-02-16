
import wx
import wx.xrc


class PanelLeft(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.Size(
                200,
                455),
            style=wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.Colour(254, 255, 254))

        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.mainButton = wx.Button(
            self,
            wx.ID_ANY,
            u">主操作界面",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.mainButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.mainButton.SetBackgroundColour(wx.Colour(120, 107, 238))
        self.mainButton.SetMinSize(wx.Size(200, 45))

        bSizerLeft.Add(self.mainButton, 0, wx.ALL, 0)

        self.addButton = wx.Button(
            self,
            wx.ID_ANY,
            u">添加搜索词",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.addButton.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.addButton.SetMinSize(wx.Size(200, 45))

        bSizerLeft.Add(self.addButton, 0, wx.ALL, 0)

        self.blockButton = wx.Button(
            self,
            wx.ID_ANY,
            u">添加屏蔽词",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.blockButton.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.blockButton.SetMinSize(wx.Size(200, 45))

        bSizerLeft.Add(self.blockButton, 0, wx.ALL, 0)

        self.SetSizer(bSizerLeft)
        self.Layout()

        # Connect Events
        self.mainButton.Bind(wx.EVT_BUTTON, self.TurnToMainFrame)
        self.mainButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterMainButton)
        self.mainButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveMainButton)
        self.addButton.Bind(wx.EVT_BUTTON, self.TrunToAddFrame)
        self.addButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterAddButton)
        self.addButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveAddButton)
        self.blockButton.Bind(wx.EVT_BUTTON, self.TurnToBlockButton)
        self.blockButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterBlockButton)
        self.blockButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveBlockButton)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def TurnToMainFrame(self, event):
        event.Skip()

    def EnterMainButton(self, event):
        event.Skip()

    def LeaveMainButton(self, event):
        event.Skip()

    def TrunToAddFrame(self, event):
        event.Skip()

    def EnterAddButton(self, event):
        event.Skip()

    def LeaveAddButton(self, event):
        event.Skip()

    def TurnToBlockButton(self, event):
        event.Skip()

    def EnterBlockButton(self, event):
        event.Skip()

    def LeaveBlockButton(self, event):
        event.Skip()
