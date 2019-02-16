import wx
import json
import PanelSearch as ps
import PanelAdd as pa
import PanelBlock as pb
import loginFrame as lf
from wx.lib.pubsub import pub


white = wx.Colour(255, 255, 255)
pink = wx.Colour(120, 107, 238)
red = wx.Colour(231, 76, 60)
black = wx.Colour(0, 0, 0)
black_pink = wx.Colour(90, 80, 180)
black_red = wx.Colour(180, 60, 50)


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)
        pass


class Frame(wx.Frame):
    def __init__(self, jsonstr):
        wx.Frame.__init__(self, parent=None, title=u'SmartSearch', size=(
            800, 500), style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        self.SetBackgroundColour(wx.Colour(238, 245, 248))
        self.SetSizeHintsSz(wx.Size(800, 500), wx.Size(800, 500))
        icon = wx.EmptyIcon()
        icon.LoadFile("image/ico.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.InitTopPanel()
        self.InitLeftPanel()
        dict = json.loads(jsonstr)
        isVerified = dict['isVerified']
        remainder = dict['remainder']
        userName = dict['userName']
        self.userId = dict['userId']
        if userName == "test":
            self.test = 1
        else:
            self.test = 0
        self.userNameText.SetLabel("你好，{}".format(userName))
        self.daysText.SetLabel("剩余天数：{}".format(remainder))
        self.okText.SetLabel("已注册")
        self.bSizerMain = wx.BoxSizer(wx.VERTICAL)
        self.bSizerMain.Add(self.PanelTop, 0, wx.ALL, 0)

        self.gbDown = wx.GridBagSizer(0, 0)
        self.gbDown.SetFlexibleDirection(wx.BOTH)
        self.gbDown.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.gbDown.Add(
            self.PanelLeft, wx.GBPosition(
                0, 0), wx.GBSpan(
                1, 1), wx.ALL, 0)
        self.PanelSearch = ps.PanelSearch(self, self.test)
        self.gbDown.Add(
            self.PanelSearch, wx.GBPosition(
                0, 1), wx.GBSpan(
                1, 1), wx.ALL, 0)
        self.bSizerMain.Add(self.gbDown, 1, wx.EXPAND, 0)
        self.nowFrame = 0
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.UpdateButton()
        self.SetSizer(self.bSizerMain)
        self.Layout()
        self.Show()

    def InitTopPanel(self):
        self.PanelTop = Panel(self)
        self.PanelTop.SetBackgroundColour(wx.Colour(44, 50, 61))
        self.PanelTop.SetMinSize(wx.Size(800, 46))

        gbSizerTop = wx.GridBagSizer(0, 0)
        gbSizerTop.SetFlexibleDirection(wx.BOTH)
        gbSizerTop.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.userNameText = wx.StaticText(
            self.PanelTop, wx.ID_ANY, u"你好，曾庆涛", wx.Point(-1, -1), wx.DefaultSize, wx.ALIGN_CENTRE)
        self.userNameText.Wrap(-1)
        self.userNameText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.userNameText.SetBackgroundColour(wx.Colour(46, 51, 62))
        self.userNameText.SetMinSize(wx.Size(180, -1))

        gbSizerTop.Add(self.userNameText, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                       wx.ALL, 10)

        self.daysText = wx.StaticText(
            self.PanelTop,
            wx.ID_ANY,
            u"剩余天数：180天",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTRE)
        self.daysText.Wrap(-1)
        self.daysText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.daysText.SetBackgroundColour(wx.Colour(45, 51, 61))
        self.daysText.SetMinSize(wx.Size(180, -1))

        gbSizerTop.Add(self.daysText, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                       wx.ALL, 10)

        self.okText = wx.StaticText(
            self.PanelTop,
            wx.ID_ANY,
            u"已注册",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTRE)
        self.okText.Wrap(-1)
        self.okText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.okText.SetBackgroundColour(wx.Colour(44, 51, 60))
        self.okText.SetMinSize(wx.Size(180, -1))

        gbSizerTop.Add(
            self.okText, wx.GBPosition(
                0, 2), wx.GBSpan(
                1, 1), wx.ALL, 10)

        self.returnButton = wx.Button(
            self.PanelTop,
            wx.ID_ANY,
            u"注销",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.returnButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.returnButton.SetBackgroundColour(wx.Colour(231, 76, 60))
        self.returnButton.SetMinSize(wx.Size(200, 45))

        gbSizerTop.Add(self.returnButton, wx.GBPosition(0, 3), wx.GBSpan(1, 1),
                       wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 0)

        self.PanelTop.SetSizer(gbSizerTop)

        # Connect Events
        self.returnButton.Bind(wx.EVT_BUTTON, self.TurnToLogin)
        self.returnButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterExitButton)
        self.returnButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveExitButton)
        pub.subscribe(self.startMessage, "lock")

    def startMessage(self, msg):
        if msg == 1:
            self.mainButton.Enable(False)
            self.addButton.Enable(False)
            self.blockButton.Enable(False)
            self.returnButton.Enable(False)
        else:
            self.mainButton.Enable()
            self.addButton.Enable()
            self.blockButton.Enable()
            self.returnButton.Enable()

    def InitLeftPanel(self):
        self.PanelLeft = Panel(self)
        self.PanelLeft.SetBackgroundColour(wx.Colour(254, 255, 254))

        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.mainButton = wx.Button(
            self.PanelLeft,
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
            self.PanelLeft,
            wx.ID_ANY,
            u">添加搜索词",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.addButton.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.addButton.SetMinSize(wx.Size(200, 45))

        bSizerLeft.Add(self.addButton, 0, wx.ALL, 0)

        self.blockButton = wx.Button(
            self.PanelLeft,
            wx.ID_ANY,
            u">添加屏蔽词",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.blockButton.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.blockButton.SetMinSize(wx.Size(200, 45))

        bSizerLeft.Add(self.blockButton, 0, wx.ALL, 0)

        self.PanelLeft.SetSizer(bSizerLeft)

        # Connect Events
        self.mainButton.Bind(wx.EVT_BUTTON, self.TurnToMainFrame)
        self.mainButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterMainButton)
        self.mainButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveMainButton)
        self.addButton.Bind(wx.EVT_BUTTON, self.TrunToAddFrame)
        self.addButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterAddButton)
        self.addButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveAddButton)
        self.blockButton.Bind(wx.EVT_BUTTON, self.TurnToBlockFrame)
        self.blockButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterBlockButton)
        self.blockButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveBlockButton)

    def OnClose(self, event):
        self.quit()
        try:
            self.tt.stop()
            del self.tt
        except BaseException:
            pass
        self.Destroy()

    def quit(self):
        import requests
        url = 'http://47.105.52.173/quit/?user={}'.format(self.userId)
        print(url)
        requests.get(url)

    def UpdateButton(self):
        self.mainButton.SetForegroundColour(black)
        self.mainButton.SetBackgroundColour(white)
        self.addButton.SetForegroundColour(black)
        self.addButton.SetBackgroundColour(white)
        self.blockButton.SetForegroundColour(black)
        self.blockButton.SetBackgroundColour(white)
        if self.nowFrame == 0:
            self.mainButton.SetForegroundColour(white)
            self.mainButton.SetBackgroundColour(pink)
        elif self.nowFrame == 1:
            self.addButton.SetForegroundColour(white)
            self.addButton.SetBackgroundColour(pink)
        else:
            self.blockButton.SetForegroundColour(white)
            self.blockButton.SetBackgroundColour(pink)

    # Virtual event handlers, overide them in your derived class

    def TurnToLogin(self, event):
        self.quit()
        self.Close()
        loginFrame = lf.loginFrame(None)

    def TurnToMainFrame(self, event):
        if self.nowFrame == 1:
            self.gbDown.Detach(self.PanelAdd)
            self.PanelAdd.Destroy()
            self.PanelSearch = ps.PanelSearch(self, self.test)
            self.gbDown.Add(
                self.PanelSearch, wx.GBPosition(
                    0, 1), wx.GBSpan(
                    1, 1), wx.ALL, 0)
            self.nowFrame = 0
            self.UpdateButton()
            self.gbDown.Layout()
        elif self.nowFrame == 2:
            self.gbDown.Detach(self.PanelBlock)
            self.PanelBlock.Destroy()
            self.PanelSearch = ps.PanelSearch(self, self.test)
            self.gbDown.Add(
                self.PanelSearch, wx.GBPosition(
                    0, 1), wx.GBSpan(
                    1, 1), wx.ALL, 0)
            self.nowFrame = 0
            self.UpdateButton()
            self.gbDown.Layout()

    def TrunToAddFrame(self, event):
        if self.nowFrame == 0:
            self.gbDown.Detach(self.PanelSearch)
            self.PanelSearch.Destroy()
            self.PanelAdd = pa.PanelAdd(self)
            self.gbDown.Add(
                self.PanelAdd, wx.GBPosition(
                    0, 1), wx.GBSpan(
                    1, 1), wx.ALL, 0)
            self.nowFrame = 1
            self.UpdateButton()
            self.gbDown.Layout()
        elif self.nowFrame == 2:
            self.gbDown.Detach(self.PanelBlock)
            self.PanelBlock.Destroy()
            self.PanelAdd = pa.PanelAdd(self)
            self.gbDown.Add(
                self.PanelAdd, wx.GBPosition(
                    0, 1), wx.GBSpan(
                    1, 1), wx.ALL, 0)
            self.nowFrame = 1
            self.UpdateButton()
            self.gbDown.Layout()

    def TurnToBlockFrame(self, event):
        if self.nowFrame == 0:
            self.gbDown.Detach(self.PanelSearch)
            self.PanelSearch.Destroy()
            del self.PanelSearch
            self.PanelBlock = pb.PanelBlock(self)
            self.gbDown.Add(
                self.PanelBlock, wx.GBPosition(
                    0, 1), wx.GBSpan(
                    1, 1), wx.ALL, 0)
            self.nowFrame = 2
            self.UpdateButton()
            self.gbDown.Layout()
        elif self.nowFrame == 1:
            self.gbDown.Detach(self.PanelAdd)
            self.PanelAdd.Destroy()
            self.PanelBlock = pb.PanelBlock(self)
            self.gbDown.Add(
                self.PanelBlock, wx.GBPosition(
                    0, 1), wx.GBSpan(
                    1, 1), wx.ALL, 0)
            self.nowFrame = 2
            self.UpdateButton()
            self.gbDown.Layout()

    def EnterMainButton(self, event):
        if self.nowFrame != 0:
            event.GetEventObject().SetForegroundColour(white)
            event.GetEventObject().SetBackgroundColour(pink)

    def LeaveMainButton(self, event):
        if self.nowFrame != 0:
            event.GetEventObject().SetForegroundColour(black)
            event.GetEventObject().SetBackgroundColour(white)

    def EnterAddButton(self, event):
        if self.nowFrame != 1:
            event.GetEventObject().SetForegroundColour(white)
            event.GetEventObject().SetBackgroundColour(pink)

    def LeaveAddButton(self, event):
        if self.nowFrame != 1:
            event.GetEventObject().SetForegroundColour(black)
            event.GetEventObject().SetBackgroundColour(white)

    def EnterBlockButton(self, event):
        if self.nowFrame != 2:
            event.GetEventObject().SetForegroundColour(white)
            event.GetEventObject().SetBackgroundColour(pink)

    def LeaveBlockButton(self, event):
        if self.nowFrame != 2:
            event.GetEventObject().SetForegroundColour(black)
            event.GetEventObject().SetBackgroundColour(white)

    # Virtual event handlers, overide them in your derived class

    def EnterExitButton(self, event):
        event.GetEventObject().SetBackgroundColour(black_red)

    def LeaveExitButton(self, event):
        event.GetEventObject().SetBackgroundColour(red)


class App(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
