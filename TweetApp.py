#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import json
from requests_oauthlib import OAuth1Session

# ここに適当に入れる
CK = ''                          # Consumer Key
CS = '' # Consumer Secret
AT = '' # Access Token
AS = ''      # Accesss Token Secert
MEDIA_URL = "https://upload.twitter.com/1.1/media/upload.json"
URL = "https://api.twitter.com/1.1/statuses/update.json"  # ツイート投稿用のURL

path = None
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window         #ファイルをドロップする対象

    def OnDropFiles(self, x, y, filenames):  #ファイルをドロップするときの処理
        for file in filenames:
            path.SetValue(file)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Twitter", size=(300, 300))
        dt = MyFileDropTarget(self)  #ドロップする対象をこのフレーム全体にする
        self.SetDropTarget(dt)

    def createImageArea(self, panel):
        global path
        path = wx.TextCtrl(panel, -1, "", size=(300,-1))
        path.Disable()

    def createButton(self, panel):
        self.button = wx.Button(panel, -1, u"Tweet", size=(300, -1))
        self.button.Bind(wx.EVT_BUTTON, self.clickButton)

    def createTextArea(self, panel):
        self.text = wx.TextCtrl(panel, -1, size=(300, 200), style=wx.TE_MULTILINE)
        self.text.Bind(wx.EVT_KEY_UP, self.onKeyPress)
        dt = MyFileDropTarget(self.text)  #ドロップする対象をこのフレーム全体にする
        self.text.SetDropTarget(dt)

    def layout(self, panel):
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(path, 0, wx.ALL, 5)
        layout.Add(self.text, 0, wx.ALL, 5)
        layout.Add(self.button, 0, wx.ALL, 5)
        panel.SetSizer(layout)

    def createParts(self):
        panel = wx.Panel(self)
        self.createImageArea(panel)
        self.createButton(panel)
        self.createTextArea(panel)
        self.layout(panel)

    def clickButton(self, event):
        self.tweet()

    def onKeyPress(self, event):
        if (event.ShiftDown() or event.CmdDown()) and 13 == event.GetKeyCode():
            self.tweet()

    def tweet(self):
        twitter = OAuth1Session(CK, CS, AT, AS)
        params = {"status": self.text.GetValue()}
        params = self.addMedia(params, twitter)
        twitter.post(URL, params=params)
        self.clearTextArea()

    def addMedia(self, params, twitter):
        if path.GetValue() != "":
            files = {"media" : open(path.GetValue(), 'rb')}
            req_media = twitter.post(MEDIA_URL, files = files)
            media_id = json.loads(req_media.text)['media_id']
            params["media_ids"] =  [media_id]
        return params

    def clearTextArea(self):
        self.text.SetValue("")
        path.SetValue("")

class TweetApp:
    def showWindow(self):
        frame = MyFrame()
        frame.createParts()
        frame.Show()

    def run(self):
        app = wx.PySimpleApp()
        self.showWindow()
        app.MainLoop()

app = TweetApp()
app.run()
