###!/usr/bin/python
#-*- coding: utf-8 -*-
#
# controler + GUI
'''*1
Belongs : YIC 情報ビジネス専門学校 情報工学科 2年
Name    : 山崎 晃弘 
E-Mail  : B0021028@ib.yic.ac.jp
'''
#
#

from controler import easyWebserver

#import tkinter
#import tkinter.ttk
#import tkinter.filedialog
from tkinter import (Widget,Toplevel,StringVar,Tk)
from tkinter.filedialog import askdirectory
from tkinter.ttk import (Label,Frame,Button,Combobox,Entry)
from threading import Thread
"""
Widget = tkinter.Widget
Toplevel = tkinter.Toplevel
StringVar = tkinter.StringVar
Tk = tkinter.Tk
askdirectory = tkinter.filedialog.askdirectory
Label    = tkinter.ttk.Label
Frame    = tkinter.ttk.Frame
Button   = tkinter.ttk.Button
Combobox = tkinter.ttk.Combobox
Entry    = tkinter.ttk.Entry
del tkinter
"""
"""
class tkWindowPlus: # tk便利化クラス
    def __init__(self) -> None:
        # ウィジェットの親ウィンドウを返す
        def personWindow(widget:Widget, Revivaled=False):
            # 自身が root か toplevel (RevivaledがTrueの時)
            if widget.master is None or (not Revivaled and type(widget) is Toplevel):
                return widget
            # 親が toplevel
            elif type(widget.master) is Toplevel:
                return widget.master
            # その他(再帰)
            else:
                return personWindow(widget.master, True)


        # 親ウィンドウのリサイズ可否を変更(変更の必要があるときのみ)
        # 変更 (したら True |しなかったら False) を返す
        # python and の 前の式が偽なら後の式が判定されない 性質使用
        self.ReSizable = lambda widget, x=False, y=False : bool(( (int(x), int(y)) != personWindow(widget).resizable() ) and personWindow(widget).resizable(x,y) is None)

        # 親ウィンドウのリサイズ
        self.ReSize = lambda widget, xy='520x280': personWindow(widget).after(10, lambda:(personWindow(widget).geometry(xy)))
        self.person = personWindow
"""

class GuiEasyWebserver:#(tkWindowPlus):
    def __init__(self, root:Tk):
        super().__init__()
        ROOT = root
        self.__cli = easyWebserver()

        ROOT.title('超簡易webサーバ')
        #self.ReSizable(ROOT)
        #self.ReSize(ROOT, "520x240")
        ROOT.geometry("320x160")

        Label(ROOT, text="Welcome").pack()

        self.root = Frame(ROOT)
        self.root.pack()


        self.refresh()
        self.mainWindow()


    def refresh(self):
        self.__cli.refresh()
        self.ip = StringVar()
        self.port = StringVar()
        self.path = StringVar()
        self.ip.set(self.__cli.ip)
        self.port.set(self.__cli.port)
        self.path.set(self.__cli.docRoot)


    def ipRefresh(self):
        self.iplist.config(values=self.__cli.ipScan())


    def __clearFrame(self):
        for x in self.root.winfo_children():
            x.destroy()
        self.root.update()


    def mainWindow(self):
        self.__clearFrame()
        self.mainFrame(self.root).pack()


    def workingWindow(self):
        self.__clearFrame()
        self.workingFrame(self.root).pack()


    def waitWindow(self, *functions):
        self.__clearFrame()
        waitFrame = Frame(self.root)
        Label(waitFrame, text="しばらくお待ち").pack()
        waitFrame.pack()
        self.root.update()
        if functions:
            for i, f in enumerate(functions):
                Thread(target=f, daemon=True).start()
                #self.root.after(10+i, f)


    def mainFrame(self, rootFrame:Frame):
        mainFrame = Frame(rootFrame)
        mainFrame.grid_rowconfigure(3,weight=1)
        mainFrame.grid_columnconfigure(0,weight=1)

        # view ip frame
        Label(mainFrame, text="待ち受けIPアドレス : ").grid(row=1,column=0)
        self.iplist = Combobox(mainFrame,textvariable=self.ip)
        self.iplist.grid(row=1,column=1)
        self.ipRefresh()
        Button(mainFrame, command=self.ipRefresh, text="IPリスト更新").grid(row=1,column=2)

        # view port frame
        Label(mainFrame, text="Port 番号 : ").grid(row=2,column=0)
        Entry(mainFrame,textvariable=self.port).grid(row=2,column=1)

        # view directory frame
        Label(mainFrame, textvariable=self.path).grid(row=3,column=0,columnspan=3)
        Button(mainFrame, command=self.chengeRootDir, text="ディレクトリ変更").grid(row=4,column=0)

        # view server start button
        Button(mainFrame, text="サーバ起動", command=lambda:self.waitWindow(self.openServer)).grid(row=4,column=1)

        return mainFrame


    def workingFrame(self, rootFrame:Frame):
        workingFrame = Frame(rootFrame)
        Label(workingFrame, text="稼働中").pack()
        for x in self.__cli.showValue().items():
            x = "{}\n{}".format(*x)
            Label(workingFrame, text=x).pack()

        Button(workingFrame, text="終了", command=lambda:self.waitWindow(self.closeServer)).pack()
        return workingFrame


    def chengeRootDir(self):
        tmp = askdirectory(initialdir = self.path.get())
        if tmp:
            self.path.set(tmp)


    # Gui Openserver before
    def openServer(self):
        flag, e = self.bootableCheck()
        if flag:
            self.__openServer()
        else:
            self.errorPopup(e)
            self.mainWindow()



    def is_openServer(self):
        return self.__cli.is_openServer()


    def bootableCheck(self):
        try:
            self.__cli.ip = self.ip.get()
            self.__cli.port = self.port.get()
            self.__cli.docRoot = self.path.get()
            return True, None
        except Exception as e:
            return False, e


    def __openServer(self):
        self.__cli.openServer()
        if not self.__cli.is_openServer():
            self.errorPopup("error not started server")
            self.mainWindow()
        else:
            self.workingWindow()


    def errorPopup(self, *args, title="Error"):
        sub_win = Toplevel()
        sub_win.geometry("300x100")
        sub_win.resizable(False,False)
        sub_win.w
        sub_win.focus_set()
        sub_win.grab_set()
        sub_win.title(title)
        for x in args:
            Label(sub_win, text=x).pack()
        Button(sub_win, text="OK", command=sub_win.destroy).pack()



    def closeServer(self):
        self.__cli.closeServer()
        for i in range(100):
            if not self.is_openServer():
                return self.mainWindow()
        self.root.after(100,self.closeServer())

def main():
    app=Tk()
    GuiEasyWebserver(app)
 
    app.mainloop()

if __name__ == "__main__":
    main()
