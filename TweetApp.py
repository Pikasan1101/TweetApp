#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import json
import csv
from requests_oauthlib import OAuth1Session
import sys
import os

filePath = None

class TokenReader:
    def __init__(self):
        self.__reader = csv.reader(open(self.resource_path("./conf/token.csv"), "r"))

    def fetchToken(self):
        tokens = {}
        for line in self.__reader:
            tokens[line[0]] = line[1]
        return tokens

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

class Tweet:
    def __init__(self):
        # ここに適当に入れる
        tokenReader = TokenReader()
        tokens = tokenReader.fetchToken()
        CK = tokens["CK"]
        CS = tokens["CS"]
        AT = tokens["AT"]
        AS = tokens["AS"]
        self.__MEDIA_URL = "https://upload.twitter.com/1.1/media/upload.json"
        self.__URL = "https://api.twitter.com/1.1/statuses/update.json"  # ツイート投稿用のURL
        self.__session = OAuth1Session(CK, CS, AT, AS)

    def tweet(self, text):
        params = {"status": text}
        params = self.addMedia(params, self.__session)
        self.__session.post(self.__URL, params=params)

    def addMedia(self, params, twitter):
        if filePath.GetValue() != "":
            files = {"media" : open(filePath.GetValue(), 'rb')}
            req_media = twitter.post(self.__MEDIA_URL, files = files)
            media_id = json.loads(req_media.text)['media_id']
            params["media_ids"] =  [media_id]
        return params

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, target):
        wx.FileDropTarget.__init__(self)
        self.target = target         #ファイルをドロップする対象

    def OnDropFiles(self, x, y, filenames):  #ファイルをドロップするときの処理
        for file in filenames:
            filePath.SetValue(file)

class MyFrame(wx.Frame):
    WINDOW_WIDTH = 200
    WINDOW_HEIGHT = 150
    # MacBook Pro 13-inchの右下 (1280,800)
    WINDOW_POSITION_X = 1280 - WINDOW_WIDTH
    WINDOW_POSITION_Y = 800 - WINDOW_HEIGHT
    
    def __init__(self):
        wx.Frame.__init__(self, None, title="Twitter", size=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pos=(self.WINDOW_POSITION_X, self.WINDOW_POSITION_Y))
        dt = MyFileDropTarget(self)  #ドロップする対象をこのフレーム全体にする
        self.SetDropTarget(dt)

    def __createImageArea(self, panel):
        global filePath
        filePath = wx.TextCtrl(panel, -1, "", size=(self.WINDOW_WIDTH,-1))
        filePath.Disable()

    def __createButton(self, panel):
        button = wx.Button(panel, -1, u"Tweet", size=(55, -1))
        button.Bind(wx.EVT_BUTTON, self.__clickButton)
        return button

    def __createTextArea(self, panel):
        text = wx.TextCtrl(panel, -1, size=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT), style=wx.TE_MULTILINE)
        text.Bind(wx.EVT_KEY_UP, self.__onKeyPress)
        dt = MyFileDropTarget(text)
        text.SetDropTarget(dt)
        return text

    def __setLayout(self, panel):
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(filePath, 0, wx.ALL, 5)
        layout.Add(self.__text, 0, wx.ALL, 5)
        layout.Add(self.__button, 0, wx.ALL, 5)
        panel.SetSizer(layout)

    def createParts(self):
        panel = wx.Panel(self)
        self.__createImageArea(panel)
        self.__button = self.__createButton(panel)
        self.__text = self.__createTextArea(panel)
        self.__setLayout(panel)

    def __clickButton(self, event):
        self.__tweet()

    def __onKeyPress(self, event):
        if (event.RawControlDown() or event.ShiftDown() or event.CmdDown()) and 13 == event.GetKeyCode():
            self.__tweet()

    def __tweet(self):
        twitter = Tweet()
        twitter.tweet(self.__text.GetValue())
        self.__clearTextArea()

    def __clearTextArea(self):
        self.__text.SetValue("")
        filePath.SetValue("")

class TweetApp:
    def __showWindow(self):
        frame = MyFrame()
        frame.createParts()
        frame.Show()

    def run(self):
        app = wx.PySimpleApp()
        self.__showWindow()
        app.MainLoop()

app = TweetApp()
app.run()
