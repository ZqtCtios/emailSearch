# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Aug 23 2015)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import sqlite3

black_pink = wx.Colour(90, 80, 180)
pink = wx.Colour(120, 107, 238)


class PanelBlock(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.Size(
                600,
                455),
            style=wx.TAB_TRAVERSAL)

        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        gbSizer = wx.GridBagSizer(0, 0)
        gbSizer.SetFlexibleDirection(wx.BOTH)
        gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.dataView = wx.grid.Grid(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.dataView.CreateGrid(50, 1)
        self.dataView.EnableEditing(True)
        self.dataView.EnableGridLines(True)
        self.dataView.EnableDragGridSize(False)
        self.dataView.SetMargins(0, 0)

        # Columns
        self.dataView.EnableDragColMove(False)
        self.dataView.EnableDragColSize(True)
        self.dataView.SetColLabelSize(30)
        self.dataView.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.dataView.EnableDragRowSize(True)
        self.dataView.SetRowLabelSize(40)
        self.dataView.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.dataView.SetColLabelValue(0, "屏蔽词")
        self.dataView.SetColSize(col=0, width=240)
        # Label Appearance

        # Cell Defaults
        self.dataView.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.dataView.SetForegroundColour(wx.Colour(0, 0, 0))
        self.dataView.SetMinSize(wx.Size(300, 400))

        gbSizer.Add(
            self.dataView, wx.GBPosition(
                0, 0), wx.GBSpan(
                1, 1), wx.ALL, 20)

        bSizer.Add(gbSizer, 1, wx.EXPAND, 5)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.editBuuton = wx.Button(
            self,
            wx.ID_ANY,
            u"确认",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.editBuuton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.editBuuton.SetBackgroundColour(wx.Colour(119, 107, 238))
        self.editBuuton.SetMinSize(wx.Size(200, 45))

        bSizer1.Add(self.editBuuton, 0, wx.ALL, 20)

        self.clearButton = wx.Button(
            self,
            wx.ID_ANY,
            u"清空",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.clearButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.clearButton.SetBackgroundColour(wx.Colour(119, 107, 238))
        self.clearButton.SetMinSize(wx.Size(200, 45))

        bSizer1.Add(self.clearButton, 0, wx.ALL, 20)

        self.message = wx.StaticText(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        self.message.Wrap(-1)
        self.message.SetForegroundColour(wx.Colour(230, 76, 60))

        bSizer1.Add(self.message, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer.Add(bSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer)
        self.Layout()

        # Connect Events
        self.editBuuton.Bind(wx.EVT_BUTTON, self.addBlockWords)
        self.editBuuton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.editBuuton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.clearButton.Bind(wx.EVT_BUTTON, self.clearBlock)
        self.clearButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.clearButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.db = sqlite3.connect('data/data.db')
        self.cursor = self.db.cursor()
        self.reFlash()

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class

    def reFlash(self):
        self.cursor.execute("select * from blockLine")
        data = self.cursor.fetchall()
        for i in range(50):
            self.dataView.SetCellValue(i, 0, '')
        length = len(data)
        for i in range(length):
            searchName = data[i][1]
            self.dataView.SetCellValue(i, 0, searchName)

    def addBlockWords(self, event):
        self.cursor.execute("delete from blockLine")
        self.cursor.execute(
            "update sqlite_sequence set seq = 0 where name =\"blockLine\"")
        self.db.commit()
        for i in range(50):
            searchName = self.dataView.GetCellValue(i, 0)
            if len(searchName) > 0:
                if searchName[-1]==' ':
                    searchName=searchName[:-1]
                self.cursor.execute(
                    "insert into blockLine(name) values (\"{}\")".format(searchName))
        self.db.commit()
        self.reFlash()

    def EnterButton(self, event):
        event.GetEventObject().SetBackgroundColour(black_pink)

    def LeaveButton(self, event):
        event.GetEventObject().SetBackgroundColour(pink)

    def clearBlock(self, event):
        dlg = wx.MessageDialog(
            None,
            "您确定要清空吗",
            "警告！！",
            wx.YES_NO | wx.ICON_QUESTION)
        reCode = dlg.ShowModal()
        if reCode == wx.ID_YES:
            self.cursor.execute("delete from blockLine")
            self.cursor.execute(
                "update sqlite_sequence set seq = 0 where name =\"blockLine\"")
            self.db.commit()
            self.reFlash()
        else:
            pass
