# -*- coding: utf-8 -*-

import wx
import wx.xrc


class PanelTop(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.Size(
                800,
                46),
            style=wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.Colour(44, 50, 61))
        self.SetMinSize(wx.Size(800, 46))

        gbSizerTop = wx.GridBagSizer(0, 0)
        gbSizerTop.SetFlexibleDirection(wx.BOTH)
        gbSizerTop.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.userNameText = wx.StaticText(
            self, wx.ID_ANY, u"你好，曾庆涛", wx.Point(-1, -1), wx.DefaultSize, wx.ALIGN_CENTRE)
        self.userNameText.Wrap(-1)
        self.userNameText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.userNameText.SetBackgroundColour(wx.Colour(46, 51, 62))
        self.userNameText.SetMinSize(wx.Size(200, -1))

        gbSizerTop.Add(self.userNameText, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                       wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 0)

        self.daysText = wx.StaticText(
            self,
            wx.ID_ANY,
            u"剩余天数：180天",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTRE)
        self.daysText.Wrap(-1)
        self.daysText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.daysText.SetBackgroundColour(wx.Colour(45, 51, 61))
        self.daysText.SetMinSize(wx.Size(200, -1))

        gbSizerTop.Add(self.daysText, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                       wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 0)

        self.okText = wx.StaticText(
            self,
            wx.ID_ANY,
            u"已注册",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTRE)
        self.okText.Wrap(-1)
        self.okText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.okText.SetBackgroundColour(wx.Colour(44, 51, 60))
        self.okText.SetMinSize(wx.Size(200, -1))

        gbSizerTop.Add(
            self.okText, wx.GBPosition(
                0, 2), wx.GBSpan(
                1, 1), wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 0)

        self.returnButton = wx.Button(
            self,
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

        self.SetSizer(gbSizerTop)
        self.Layout()

        # Connect Events
        self.returnButton.Bind(wx.EVT_BUTTON, self.TurnToLogin)
        self.returnButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterExitButton)
        self.returnButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveExitButton)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def TurnToLogin(self, event):
        event.Skip()

    def EnterExitButton(self, event):
        event.Skip()

    def LeaveExitButton(self, event):
        event.Skip()
