#!/usr/bin/python
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

import tkinter as tk
from tkinter import ttk, filedialog




class tkWindowPlus: # tk便利化クラス
    def __init__(self) -> None:
        # ウィジェットの親ウィンドウを返す
        def personWindow(widget:tk.Widget, Revivaled=False):
            # 自身が root (か toplevel (RevivaledがTrueの時)
            if widget.master is None or (not Revivaled and type(widget) is tk.Toplevel):
                return widget
            # 親が toplevel
            elif type(widget.master) is tk.Toplevel:
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



class GuiEasyWebserver(tkWindowPlus):
    def __init__(self, root:tk.Tk):
        super().__init__()
        ROOT = root
        self.__cli = easyWebserver()

        ROOT.title('超簡易webサーバ')
        self.ReSizable(ROOT)
        self.ReSize(ROOT, "720x240")

        ttk.Label(ROOT, text="Welcome").pack()

        self.root = ttk.Frame(ROOT)
        self.root.pack()


        self.refresh()
        self.mainWindow()


    def refresh(self):
        self.__cli.refresh()
        self.ip = tk.StringVar()
        self.port = tk.StringVar()
        self.path = tk.StringVar()
        self.ip.set(self.__cli.ip)
        self.port.set(self.__cli.port)
        self.path.set(self.__cli.docRoot)


    def ipRefresh(self):
        self.iplist.config(values=self.__cli.ipScan())


    def __clearFrame(self):
        for x in self.root.winfo_children():
            x.destroy()


    def mainWindow(self):
        self.__clearFrame()
        self.mainFrame(self.root).pack()


    def workingWindow(self):
        self.__clearFrame()
        self.workingFrame(self.root).pack()


    def waitWindow(self, *functions):
        self.__clearFrame()
        waitFrame = ttk.Frame(self.root)
        ttk.Label(waitFrame, text="しばらくお待ち").pack()
        waitFrame.pack()
        if functions:
            for i, f in enumerate(functions):
                self.root.after(10+i, f)


    def mainFrame(self, rootFrame:ttk.Frame):
        mainFrame = ttk.Frame(rootFrame)
        mainFrame.grid_rowconfigure(3,weight=1)
        mainFrame.grid_columnconfigure(0,weight=1)

        # view ip frame
        ttk.Label(mainFrame, text="待ち受けIPアドレス : ").grid(row=1,column=0)
        self.iplist = ttk.Combobox(mainFrame,textvariable=self.ip)
        self.iplist.grid(row=1,column=1)
        self.ipRefresh()
        ttk.Button(mainFrame, command=self.ipRefresh, text="IPリスト更新").grid(row=1,column=2)

        # view port frame
        ttk.Label(mainFrame, text="Port 番号 : ").grid(row=2,column=0)
        ttk.Entry(mainFrame,textvariable=self.port).grid(row=2,column=1)

        # view directory frame
        ttk.Label(mainFrame, textvariable=self.path).grid(row=3,column=0)
        ttk.Button(mainFrame, command=self.chengeRootDir, text="ディレクトリ変更").grid(row=4,column=0)

        # view server start button
        ttk.Button(mainFrame, text="サーバ起動", command=lambda:self.waitWindow(self.openServer)).grid(row=4,column=1)

        return mainFrame


    def workingFrame(self, rootFrame:ttk.Frame):
        workingFrame = tk.Frame(rootFrame)
        ttk.Label(workingFrame, text="稼働中").pack()
        for x in self.__cli.showValue().items():
            ttk.Label(workingFrame, text=x).pack()
        ttk.Button
        ttk.Button(workingFrame, text="終了", command=lambda:self.waitWindow(self.closeServer, self.mainWindow)).pack()
        return workingFrame


    def chengeRootDir(self):
        tmp = filedialog.askdirectory(initialdir = self.path.get())
        if tmp:
            self.path.set(tmp)


    # Gui Openserver before
    def openServer(self):
        self.waitWindow()
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
        sub_win = tk.Toplevel()
        self.ReSize(sub_win, "300x100")
        self.ReSizable(sub_win)
        sub_win.focus_set()
        sub_win.grab_set()
        sub_win.title(title)
        for x in args:
            ttk.Label(sub_win, text=x).pack()
        ttk.Button(sub_win, text="OK", command=sub_win.destroy).pack()
        pass


    def closeServer(self):
        self.__cli.closeServer()


def main():
    app=tk.Tk()
    GuiEasyWebserver(app)
    app.mainloop()

if __name__ == "__main__":
    main()
