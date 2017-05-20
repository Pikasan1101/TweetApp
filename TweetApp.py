#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import json
import csv
from PIL import Image
from requests_oauthlib import OAuth1Session

class TokenReader:
    def __init__(self):
        self.__reader = csv.reader(open("token.csv", "r"))

    def fetchToken(self):
        tokens = {}
        for line in self.__reader:
            tokens[line[0]] = line[1]
        return tokens

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

    def tweet(self, text, mediaHolder):
        params = {"status": text}
        params = self.addMedia(params, self.__session, mediaHolder)
        self.__session.post(self.__URL, params=params)

    def addMedia(self, params, session, mediaHolder):
        media_ids = []
        if len(mediaHolder.files) > 4:
            for filePath, image in mediaHolder.files.items()[:4]:
                files = {"media" : open(filePath, 'rb')}
                req_media = session.post(self.__MEDIA_URL, files=files)
                media_id = json.loads(req_media.text)['media_id']
                media_ids.append(media_id)
        else:
            for filePath, image in mediaHolder.files.items():
                files = {"media" : open(filePath, 'rb')}
                req_media = session.post(self.__MEDIA_URL, files=files)
                media_id = json.loads(req_media.text)['media_id']
                media_ids.append(media_id)
        params["media_ids"] = ",".join(list(map(str, media_ids)))
        return params

class MediaHolder:
    def __init__(self, frame):
        self.files = {}
        self.__frame = frame
        self.__currentShowFile0 = None
        self.__currentShowFile1 = None
        self.__currentShowFile2 = None
        self.__currentShowFile3 = None

    def add(self, filePath):
        image_pil = Image.open(filePath)
        image_pil.thumbnail((60,60), Image.ANTIALIAS)
        image = wx.EmptyImage(image_pil.size[0],image_pil.size[1])
        image.SetData(image_pil.convert('RGB').tobytes())
        self.files[filePath] = image

    def reset(self):
        self.files = {}
        try:
            self.__currentShowFile0.Hide()
            self.__currentShowFile1.Hide()
            self.__currentShowFile2.Hide()
            self.__currentShowFile3.Hide()
        except:
            pass
        self.__currentShowFile0 = None
        self.__currentShowFile1 = None
        self.__currentShowFile2 = None
        self.__currentShowFile3 = None

    def remove0(self, event):
        filePath, image = self.files.items()[0]
        del self.files[filePath]
        self.__currentShowFile0.Hide()
        self.show()
    def remove1(self, event):
        filePath, image = self.files.items()[1]
        del self.files[filePath]
        self.__currentShowFile1.Hide()
        self.show()
    def remove2(self, event):
        filePath, image = self.files.items()[2]
        del self.files[filePath]
        self.__currentShowFile2.Hide()
        self.show()
    def remove3(self, event):
        filePath, image = self.files.items()[3]
        del self.files[filePath]
        self.__currentShowFile3.Hide()
        self.show()

    def show(self):
        try:
            self.__currentShowFile0.Hide()
            self.__currentShowFile1.Hide()
            self.__currentShowFile2.Hide()
            self.__currentShowFile3.Hide()
        except:
            pass
        try:
            filePath, image = self.files.items()[0]
            self.__currentShowFile0 = wx.StaticBitmap(self.__frame, -1, image.ConvertToBitmap(), (0,0), (640,480))
            self.__currentShowFile0.Bind(wx.EVT_LEFT_DOWN, self.remove0)
            filePath, image = self.files.items()[1]
            self.__currentShowFile1 = wx.StaticBitmap(self.__frame, -1, image.ConvertToBitmap(), (70,0), (640,480))
            self.__currentShowFile1.Bind(wx.EVT_LEFT_DOWN, self.remove1)
            filePath, image = self.files.items()[2]
            self.__currentShowFile2 = wx.StaticBitmap(self.__frame, -1, image.ConvertToBitmap(), (140,0), (640,480))
            self.__currentShowFile2.Bind(wx.EVT_LEFT_DOWN, self.remove2)
            filePath, image = self.files.items()[3]
            self.__currentShowFile3 = wx.StaticBitmap(self.__frame, -1, image.ConvertToBitmap(), (210,0), (640,480))
            self.__currentShowFile3.Bind(wx.EVT_LEFT_DOWN, self.remove3)
        except:
            pass

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, frame, mediaHolder):
        wx.FileDropTarget.__init__(self)
        self.__frame = frame         #ファイルをドロップする対象
        self.__mediaHolder = mediaHolder
        self.images = []

    def OnDropFiles(self, x, y, files):  #ファイルをドロップするときの処理
        for filePath in files:
            self.__mediaHolder.add(filePath)
        self.__mediaHolder.show()

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Twitter", size=(300, 300))
        self.__mediaHolder = MediaHolder(self)
        dt = MyFileDropTarget(self, self.__mediaHolder)  #ドロップする対象をこのフレーム全体にする
        self.SetDropTarget(dt)

    def __createImageArea(self, panel):
        self.filePath = wx.TextCtrl(panel, -1, "", size=(300,-1))
        self.filePath.Disable()

    def __createButton(self, panel):
        button = wx.Button(panel, -1, u"Tweet", size=(280, -1), pos=(10, 240))
        button.Bind(wx.EVT_BUTTON, self.__clickButton)
        return button

    def __createTextArea(self, panel):
        text = wx.TextCtrl(panel, -1, size=(280, 130), style=wx.TE_MULTILINE, pos=(10, 100))
        text.Bind(wx.EVT_KEY_UP, self.__onKeyPress)
        dt = MyFileDropTarget(self, self.__mediaHolder)
        text.SetDropTarget(dt)
        return text

    def __setLayout(self, panel):
        layout = wx.BoxSizer(wx.VERTICAL)
        # layout.Add(self.filePath, 0, wx.ALL, 5)
        layout.Add(self.__text, 0, wx.ALL, 5)
        layout.Add(self.__button, 0, wx.ALL, 5)
        panel.SetSizer(layout)

    def createParts(self):
        panel = wx.Panel(self)
        # self.__createImageArea(panel)
        self.__button = self.__createButton(panel)
        self.__text = self.__createTextArea(panel)
        # self.__setLayout(panel)

    def __clickButton(self, event):
        self.__tweet()

    def __onKeyPress(self, event):
        if (event.RawControlDown() or event.ShiftDown() or event.CmdDown()) and 13 == event.GetKeyCode():
            self.__tweet()

    def __tweet(self):
        twitter = Tweet()
        twitter.tweet(self.__text.GetValue(), self.__mediaHolder)
        self.__clearTextArea()

    def __clearTextArea(self):
        self.__text.SetValue("")
        self.__mediaHolder.reset()
        # self.filePath.SetValue("")

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
