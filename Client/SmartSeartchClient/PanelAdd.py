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
###########################################################################
# Class PanelAdd
###########################################################################


class PanelAdd(wx.Panel):

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

        self.addDataView = wx.grid.Grid(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.addDataView.CreateGrid(20, 1)
        self.addDataView.EnableEditing(True)
        self.addDataView.EnableGridLines(True)
        self.addDataView.EnableDragGridSize(False)
        self.addDataView.SetMargins(0, 0)

        # Columns
        self.addDataView.EnableDragColMove(False)
        self.addDataView.EnableDragColSize(True)
        self.addDataView.SetColLabelSize(30)
        self.addDataView.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.addDataView.EnableDragRowSize(True)
        self.addDataView.SetRowLabelSize(40)
        self.addDataView.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.addDataView.SetColLabelValue(0, "搜索词")
        self.addDataView.SetColSize(col=0, width=240)
        # Label Appearance

        # Cell Defaults
        self.addDataView.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.addDataView.SetMinSize(wx.Size(300, 400))

        gbSizer.Add(
            self.addDataView, wx.GBPosition(
                0, 0), wx.GBSpan(
                1, 1), wx.ALL, 20)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.addEditBuuton = wx.Button(
            self,
            wx.ID_ANY,
            u"确认",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.addEditBuuton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.addEditBuuton.SetBackgroundColour(wx.Colour(119, 107, 238))
        self.addEditBuuton.SetMinSize(wx.Size(200, 45))

        bSizer1.Add(self.addEditBuuton, 0, wx.ALL, 20)

        self.addClearButton = wx.Button(
            self,
            wx.ID_ANY,
            u"清空",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.addClearButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.addClearButton.SetBackgroundColour(wx.Colour(119, 107, 238))
        self.addClearButton.SetMinSize(wx.Size(200, 45))

        bSizer1.Add(self.addClearButton, 0, wx.ALL, 20)

        self.okMessage = wx.StaticText(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        self.okMessage.Wrap(-1)
        bSizer1.Add(self.okMessage, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer.Add(
            bSizer1, wx.GBPosition(
                0, 1), wx.GBSpan(
                1, 1), wx.EXPAND, 5)

        bSizer.Add(gbSizer, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer)
        self.Layout()

        # Connect Events
        self.addEditBuuton.Bind(wx.EVT_BUTTON, self.addSearchWord)
        self.addEditBuuton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.addEditBuuton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.addClearButton.Bind(wx.EVT_BUTTON, self.clearWords)
        self.addClearButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.addClearButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.db = sqlite3.connect('data/data.db')
        self.cursor = self.db.cursor()
        self.reFlash()

    def __del__(self):
        pass

    def reFlash(self):
        self.cursor.execute("select * from searchLine where hasDone=0")
        data = self.cursor.fetchall()
        length = len(data)
        for i in range(20):
            self.addDataView.SetCellValue(i, 0, '')
        for i in range(length):
            searchName = data[i][1]
            self.addDataView.SetCellValue(i, 0, searchName)

    def addSearchWord(self, event):
        self.cursor.execute("delete from searchLine")
        self.cursor.execute(
            "update sqlite_sequence set seq = 0 where name =\"searchLine\"")
        self.db.commit()
        for i in range(20):
            searchName = self.addDataView.GetCellValue(i, 0)
            if len(searchName) > 0:
                if searchName[-1]==' ':
                    searchName=searchName[:-1]
                self.cursor.execute(
                    "insert into searchLine(name,hasDone) values (\"{}\",0)".format(searchName))
        self.db.commit()
        self.reFlash()

    def EnterButton(self, event):
        event.GetEventObject().SetBackgroundColour(black_pink)

    def LeaveButton(self, event):
        event.GetEventObject().SetBackgroundColour(pink)

    def clearWords(self, event):
        dlg = wx.MessageDialog(
            None,
            "您确定要清空吗",
            "警告！！",
            wx.YES_NO | wx.ICON_QUESTION)
        reCode = dlg.ShowModal()
        if reCode == wx.ID_YES:
            self.cursor.execute("delete from searchLine")
            self.cursor.execute(
                "update sqlite_sequence set seq = 0 where name =\"searchLine\"")
            self.db.commit()
            self.reFlash()
        else:
            pass
