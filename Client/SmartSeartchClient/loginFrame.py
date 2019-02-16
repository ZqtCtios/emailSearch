# -*- coding: utf-8 -*-


import wx
import wx.xrc
import mainFrame
import requests
import sqlite3
import json
black_red = wx.Colour(180, 60, 50)
red = wx.Colour(231, 76, 60)


class loginFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=u"Login",
            pos=wx.DefaultPosition,
            size=wx.Size(
                400,
                340),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.Size(400, 340), wx.Size(400, 370))
        self.SetBackgroundColour(wx.Colour(46, 51, 62))
        icon = wx.EmptyIcon()
        icon.LoadFile("image/ico.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.logoImg = wx.StaticBitmap(
            self,
            wx.ID_ANY,
            wx.Bitmap(
                u"image/logo.jpg",
                wx.BITMAP_TYPE_ANY),
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        bSizer9.Add(self.logoImg, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.logoUserName = wx.StaticBitmap(
            self,
            wx.ID_ANY,
            wx.Bitmap(
                u"image/userLogo.jpg",
                wx.BITMAP_TYPE_ANY),
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        bSizer10.Add(self.logoUserName, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        self.userNameInput = wx.TextCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        self.userNameInput.SetForegroundColour(wx.Colour(255, 255, 255))
        self.userNameInput.SetBackgroundColour(wx.Colour(45, 51, 61))
        self.userNameInput.SetMinSize(wx.Size(180, -1))

        bSizer10.Add(self.userNameInput, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        bSizer9.Add(bSizer10, 1, wx.ALIGN_CENTER | wx.ALL, 0)

        bSizer11 = wx.BoxSizer(wx.HORIZONTAL)

        self.logoPasswd = wx.StaticBitmap(
            self,
            wx.ID_ANY,
            wx.Bitmap(
                u"image/passwdLogo.jpg",
                wx.BITMAP_TYPE_ANY),
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        bSizer11.Add(self.logoPasswd, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        self.passwdInput = wx.TextCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_PASSWORD)
        self.passwdInput.SetForegroundColour(wx.Colour(255, 255, 255))
        self.passwdInput.SetBackgroundColour(wx.Colour(46, 51, 62))
        self.passwdInput.SetMinSize(wx.Size(180, -1))

        bSizer11.Add(self.passwdInput, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        bSizer9.Add(bSizer11, 1, wx.ALIGN_CENTER, 0)

        self.message = wx.StaticText(
            self,
            wx.ID_ANY,
            u"请输入账号密码",
            wx.DefaultPosition,
            wx.DefaultSize,
            0)
        self.message.Wrap(-1)
        self.message.SetForegroundColour(wx.Colour(255, 0, 0))
        self.message.SetBackgroundColour(wx.Colour(46, 51, 61))

        bSizer9.Add(self.message, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.loginButton = wx.Button(
            self,
            wx.ID_ANY,
            u"登陆",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NO_BORDER)
        self.loginButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.loginButton.SetBackgroundColour(wx.Colour(231, 76, 60))
        self.loginButton.SetMinSize(wx.Size(200, 45))

        bSizer9.Add(self.loginButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer9)
        self.Layout()

        self.Centre(wx.BOTH)
        self.db = sqlite3.connect("data/data.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.showUser()
        # Connect Events
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        self.loginButton.Bind(wx.EVT_ENTER_WINDOW, self.EnterButton)
        self.loginButton.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveButton)
        self.Show()

    def __del__(self):
        pass

    def showUser(self):
        self.cursor.execute("select * from userData")
        data = self.cursor.fetchall()
        if len(data) == 0:
            return
        username = data[0][1]
        passwd = data[0][2]
        self.userNameInput.SetValue(username)
        self.passwdInput.SetValue(passwd)

    def test(self, user, passwd):
        try:
            url = 'http://47.105.52.173/verify/?user={}&passwd={}'.format(
                user, passwd)
            html = requests.get(url).text
            if len(html) < 10:
                return 0, html
            return 1, html
        except BaseException:
            return 2, '{}'
    # Virtual event handlers, overide them in your derived class

    def login(self, event):
        userName = self.userNameInput.GetValue()
        passwd = self.passwdInput.GetValue()
        anser, jsonStr = self.test(userName, passwd)
        if userName == "test":
            self.cursor.execute("select * from test")
            data = self.cursor.fetchall()
            if data[0][0]:
                self.message.SetLabel("测试账户以过期请重新购买")
                return
        if anser == 0:
            self.message.SetLabel("用户名或密码错误")
        elif anser == 2:
            self.message.SetLabel("连接服务器失败")
        else:
            dic = json.loads(jsonStr)
            hasLogin = dic['loginFlag']
            remainder = dic['remainder']
            if remainder == 0 and userName != 'test':
                self.message.SetLabel("该账号已逾期，请重新购买")
                return
            print(hasLogin)
            if hasLogin == 1:
                self.message.SetLabel("该账号已登陆,若非本人请联系管理员")
                return
            self.message.SetLabel("登陆成功")
            self.Close()
            self.cursor.execute("delete from userData")
            self.cursor.execute(
                "update sqlite_sequence set seq = 0 where name =\"userData\"")
            self.cursor.execute(
                "insert into userData(userName, passwd) values (\"{}\",\"{}\")".format(
                    userName, passwd))
            self.db.commit()
            mainF = mainFrame.Frame(jsonStr)

    def EnterButton(self, event):
        event.GetEventObject().SetBackgroundColour(black_red)

    def LeaveButton(self, event):
        event.GetEventObject().SetBackgroundColour(red)


if __name__ == '__main__':
    app = wx.App(False)
    frame = loginFrame(None)
    app.MainLoop()
