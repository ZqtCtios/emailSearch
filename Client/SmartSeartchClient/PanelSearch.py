# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Aug 23 2015)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import SearchThread
from wx.lib.pubsub import pub
import os
import sqlite3
black_pink = wx.Colour(90, 80, 180)
pink = wx.Colour(120, 107, 238)


class PanelSearch(wx.Panel):

    def __init__(self, parent, test):
        wx.Panel.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.Size(
                600,
                455),
            style=wx.TAB_TRAVERSAL)

        self.SetMinSize(wx.Size(600, 455))
        self.SetBackgroundColour(wx.Colour(238, 245, 248))
        self.test = test
        bSizer = wx.BoxSizer(wx.VERTICAL)

        gbSizer = wx.GridBagSizer(0, 0)
        gbSizer.SetFlexibleDirection(wx.BOTH)
        gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.message = wx.TextCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE | wx.TE_READONLY)
        self.message.SetMinSize(wx.Size(580, 300))

        gbSizer.Add(
            self.message, wx.GBPosition(
                1, 0), wx.GBSpan(
                1, 1), wx.ALL, 5)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.startButton = wx.Button(
            self,
            wx.ID_ANY,
            u"开始",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.startButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.startButton.SetBackgroundColour(wx.Colour(119, 107, 238))
        self.startButton.SetMinSize(wx.Size(400, 60))

        bSizer1.Add(self.startButton, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.openButton = wx.Button(
            self,
            wx.ID_ANY,
            u"打开输出文件夹",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.openButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.openButton.SetBackgroundColour(wx.Colour(119, 106, 237))
        self.openButton.SetMinSize(wx.Size(150, 60))

        bSizer1.Add(self.openButton, 0, wx.ALL, 10)

        gbSizer.Add(
            bSizer1, wx.GBPosition(
                2, 0), wx.GBSpan(
                1, 1), wx.ALIGN_CENTER | wx.EXPAND, 10)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.StaticText(
            self,
            wx.ID_ANY,
            u"信息输出框：",
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        self.text.Wrap(-1)
        self.text.SetForegroundColour(wx.Colour(0, 0, 0))

        bSizer2.Add(self.text, 0, wx.ALL, 5)

        gbSizer.Add(
            bSizer2, wx.GBPosition(
                0, 0), wx.GBSpan(
                1, 1), wx.EXPAND, 5)

        bSizer.Add(gbSizer, 1, wx.EXPAND, 5)
        self.ok = 0
        self.SetSizer(bSizer)
        self.Layout()
        self.db = sqlite3.connect("data/data.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        # Connect Events
        self.startButton.Bind(wx.EVT_BUTTON, self.startWork)
        self.startButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.startButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.openButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.openButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.openButton.Bind(wx.EVT_BUTTON, self.openDir)
        pub.subscribe(self.updateDisplay, "update")

    def __del__(self):
        try:
            self.tt.stop()
            del self.tt
        except BaseException:
            pass

    def openDir(self, event):
        path = os.path.join(os.path.dirname(__file__), 'OutPut')
        print(path)
        os.system("explorer {}".format(path))

    # Virtual event handlers, overide them in your derived class
    def startWork(self, event):
        if self.ok == 0:
            self.cursor.execute("select * from test")
            data = self.cursor.fetchall()
            if data[0][0]:
                self.message.AppendText("测试账号只允许测试一次")
                return
            self.tt = SearchThread.TestThread(self.test)
            self.tt.start()
            self.startButton.SetLabel("停止")
            self.ok = 1
        else:
            self.ok = 0
            self.tt.stop()
            self.startButton.Enable(False)

    def updateDisplay(self, msg):
        t = msg
        if t == 0:
            self.message.AppendText("停止")
            self.startButton.Enable()
            self.startButton.SetLabel("开始")
        else:
            self.message.AppendText(msg)

    def EnterButton(self, event):
        event.GetEventObject().SetBackgroundColour(black_pink)

    def LeaveButton(self, event):
        event.GetEventObject().SetBackgroundColour(pink)
