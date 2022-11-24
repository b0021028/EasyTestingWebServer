#!/usr/bin/python
#-*- coding: utf-8 -*-
#
#
'''*1
Belongs : YIC 情報ビジネス専門学校 情報工学科 2年
Name    : 山崎 晃弘 
E-Mail  : B0021028@ib.yic.ac.jp
'''
#
#

from http.server import (
    SimpleHTTPRequestHandler,
    ThreadingHTTPServer,
    CGIHTTPRequestHandler
)


# path と query と fragment を切り分ける
def splitURN(pathAndQuery="/") -> dict[str, str, str]:
    """path と query"?" と fragment"#" を切り分ける"""
    path, _, fragment = str(pathAndQuery).partition("#")
    path, _, query = path.partition("?")
    if fragment:
        print(RuntimeWarning(RuntimeError(f"Why coul'd getting 'url fragment'? fragment:{fragment}")))

    return {"path":path, "query":query, "fragment":fragment}


# URLデコーダー
def decodeURL(txt):
    from urllib.parse import unquote
    return unquote(txt)



CGIHTTPRequestHandler.protocol_version = "HTTP/1.1"
CGIHTTPRequestHandler.cgi_directories = []
class CustomCGI(CGIHTTPRequestHandler):
    def is_cgi(self):
        filename = splitURN(self.path)["path"].rpartition("/")
        print(filename, self.path, sep=" [@] ")
        if filename[-1].rpartition(".")[-1] == "py":
            self.cgi_info = (filename[0::2])
            return True
        return False
        #('/ftpserver/testsite', 'testcgi.py')

    def send_head(self):
        if self.is_cgi():
            return self.run_cgi()
        else:
            return SimpleHTTPRequestHandler.send_head(self)

class DualStackServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], RequestHandlerClass, bind_and_activate: bool = ..., _rootDir:str|None=None) -> None:
        self._docRoot_dir = _rootDir
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(
            request, client_address, self,
            directory=self._docRoot_dir
            )

DualStackServer.address_family = 2


def serverSaving(ip:str="0.0.0.0", port:int=8080, dir:str|None=None):
    return DualStackServer((ip, port), CustomCGI, _rootDir=dir)



if __name__ == "__main__":
    splitURN("/afesaf/fase/fa?fa#fae")






if False:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from os import path as filepath
    import tkinter as tk
    from tkinter import ttk, filedialog

    class tkWindowPlus: # tk便利化クラス
        def __init__(self) -> None:
            from tkinter import Toplevel, Widget
            # ウィジェットの親ウィンドウを返す
            def personWindow(widget:Widget, Revivaled=False):

                # 自身が root (か toplevel (RevivaledがTrueの時)
                if widget.master is None or (not Revivaled and type(widget) is Toplevel):
                    return widget
                # 親が toplevel
                elif type(widget.master) is Toplevel:
                    return widget.master
                # その他(再帰)
                else:
                    return personWindow(widget.master, True)

            def ReSizable(widget, x=False, y=False):
                x, y = map(int, (x, y))
                widget = personWindow(widget)
                if (x, y) != widget.resizable():
                    widget.resizable(x,y)
                    return True
                return False

            def ReSize(widget, xy='520x280'):
                personWindow(widget).after(10, lambda:(
                    personWindow(widget).geometry(xy)
                    ))

            # 親ウィンドウのリサイズ可否を変更(変更の必要があるときのみ)
            # 変更 (したら True |しなかったら False) を返す
            # python and の 前の式が偽なら後の式が判定されない 性質使用
            self.ReSizable = lambda widget, x=False, y=False : bool(( (int(x), int(y)) != personWindow(widget).resizable() ) and personWindow(widget).resizable(x,y) is None)

            # 親ウィンドウのリサイズ
            self.ReSize = lambda widget, xy='520x280': personWindow(widget).after(10, lambda:(personWindow(widget).geometry(xy)))
            self.person = personWindow


    class easyWebserver(tkWindowPlus):
        class IPAddrError(ValueError):pass
        class PortError(ValueError):pass
        def __init__(self):
            super().__init__()
            ROOT = tk.Tk()
            self.mainloop=lambda:ROOT.mainloop()

            ROOT.title('超簡易webサーバ')
            self.ReSizable(ROOT)
            self.ReSize(ROOT, "520x320")

            self.root = ttk.Frame(ROOT)
            self.root.pack()

            self.refresh()
            self.mainWindow()


        def refresh(self):
            dprint(self.root.children)
            self.ip = tk.StringVar()
            self.ip.set("0.0.0.0")
            self.port = tk.StringVar()
            self.port.set(8080)
            self.path = tk.StringVar()
            self.path.set(__file__.rpartition("\\")[0])


        def ipScan(self) -> tuple[str,...]:
            from socket import gethostname, gethostbyname_ex
            return (*gethostbyname_ex(gethostname())[2], "0.0.0.0")

        def ipRefresh(self):
            self.iplist.config(values=self.ipScan())

        def mainWindow(self):
            ttk.Label(self.root, text="Welcome").pack()
            sb2_frame = ttk.Frame(self.root)

            ttk.Label(sb2_frame, text="待ち受けIPアドレス : ").grid(row=1,column=0)
            self.iplist = ttk.Combobox(sb2_frame,textvariable=self.ip)
            self.iplist.grid(row=1,column=1)
            self.ipRefresh()
            ttk.Button(sb2_frame, command=self.ipRefresh, text="IPリスト更新").grid(row=1,column=2)

            ttk.Label(sb2_frame, text="Port 番号 : ").grid(row=2,column=0)
            ttk.Entry(sb2_frame,textvariable=self.port).grid(row=2,column=1)

            
            ttk.Label(sb2_frame, textvariable=self.path).grid(row=3,column=0)
            ttk.Button(sb2_frame, command=self.chengeRootDir, text="ディレクトリ変更").grid(row=3,column=1)
            

            ttk.Button(sb2_frame, command=self.__openServer, text="サーバ起動").grid(row=3,column=2)

            sb2_frame.pack()
            pass

        def chengeRootDir(self):
            self.path.set(filedialog.askdirectory(initialdir = self.path.get()))

        # Gui Openserver before
        def __openServer(self):
            try:
                IP, PORT = self.bootableCheck(self.ip.get(), self.port.get())
            except ImportError:
                raise ImportError("Fatal Error (bootableCheck[import error])")
            except easyWebserver.IPAddrError:
                return self.errorPopup("IPAddress is Faild.", "IP is selected by list.")
            except easyWebserver.PortError:
                return self.errorPopup("Port Number is Faild.", "Port Number is 1~65535.")
            return self.openServer(IP, PORT)
            
        # Cui&Gui ip and port before checker
        def bootableCheck(self, ip, port):
            # インポート
            try:
                from ipaddress import ip_address
            except ImportError:
                raise ImportError("Fatal Error (bootableCheck[import error])")

            try:
                IP = ip_address(ip)
                if not f"{IP}" in self.ipScan():
                    raise ValueError
            except ValueError:
                raise easyWebserver.IPAddrError

            try:
                PORT = int(port)
                if f"{PORT}" != f"{port}" or not (0 < PORT < 65536):
                    raise ValueError
            except ValueError:
                raise easyWebserver.PortError

            return (IP, PORT)


        def openServer(self, ip, port):
            dprint(ip, port)
            pass

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

    def mainWindow():
        easyWebserver().mainloop()

    mainWindow()

if False:
    # 定数
    # ウェブサーバのルートディレクトリ 例 www/html 例2　/usr/share/www/html 例3 ../html デフォルトで filepath.dirname(__file__) + "/."
    # This program   file path    is [filepath.dirname(__file__)]
    # executed shell current path is [.]
    ROOTDIRECTORY = filepath.dirname(__file__) + "/."

    # ウェブサーバの待ち受けipアドレスと待ち受けポート
    BIND_IP, BIND_PORT = "127.0.0.1", 8000

    INDEXFILE = "index.html",



    # path と query と fragment を切り分ける
    def splitURN(pathAndQuery="/") -> dict[str, str]:
        """path と query"?" と fragment"#" を切り分ける"""
        path, _, fragment = str(pathAndQuery).partition("#")
        path, _, query = path.partition("?")

        return {"path":path, "query":query, "fragment":fragment}

    # URLデコーダー
    def decodeURL(txt):
        from urllib.parse import unquote
        return unquote(txt)


    # server 本体
    class CustomHandler(SimpleHTTPRequestHandler):


        def do_GET(self):
            # 処理できないものはデフォルトに頼る
            
            # 要求された path を取得し クエリ―と分けて ルートdirをパスに追加
            path = splitURN(self.path)["path"]
            path = decodeURL(path)
            path = ROOTDIRECTORY + (path[:-1] if path[-1] == '/' else path)
            dprint(self.command)
            dprint(f"^=\nrequest    : {splitURN(self.path)}\nanalyzePath : {path}\n=$")
            responseText = ""
            byteResponce = b""

            # イースターエッグ
            if "//" in self.path:
                # responseText の 作成
                responseText += "<h1>Easter Egg</h1><ul>"
                for x in splitURN(self.path).items():
                    responseText += f"<li><p>{x[0]}</p><p>"
                    responseText += f"'{x[1]}'" if x[1] else "None"
                    responseText += "</p></li>"
                responseText += "<li><p>urn default read sin</p><p><a href=\"/!$%&'()=~*+_-/@[;:],./////\">!$%&'()=~*+_-/@[;:],.</p></li>"
                responseText += "</ul>"


                # ヘッダー作成
                self.send_response(200, "OK Easter-Egg>(^^)/")
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache")
                # responseText の byte変換
                byteResponce = bytes(responseText, encoding="utf-8")


            elif filepath.exists(path):

                # ファイルは 存在すれば 開く
                if filepath.isfile(path):

                    # ファイルからテキスト読み込み
                    # file type check
                    filetype = self.guess_type(self.path)
                    dprint(filetype)
                    if "text" in filetype:
                        responseText = open(path, encoding="utf-8").read()

                        # ヘッダー作成
                        self.send_response(200, "OK")
                        self.send_header("Content-type", f"{filetype}; charset=utf-8")
                        # responseText の byte変換
                        byteResponce = bytes(responseText, encoding="utf-8")

                    elif filepath.splitext(path)[1] == "":
                        responseText = open(path, encoding="utf-8").read()
                        # ヘッダー作成
                        self.send_response(200, "OK")
                        self.send_header("Content-type", "text/plain; charset=utf-8")
                        # responseText の byte変換
                        byteResponce = bytes(responseText, encoding="utf-8")


                    elif filetype.split("/")[0] in ("image", "audio", "video"): # 実験
                        self.send_response(200, "OK")
                        self.send_header("Content-type", f"{filetype};")
                        # responseText の byte変換
                        byteResponce = open(path, "rb").read()
                    # unknown Type file

                    else:
                        dprint(f"unknown type file super:{self.path}")
                        return super().do_GET()


                # ディレクトリは INDEXFILE を開く ない場合 dirlist を見せる
                elif filepath.isdir(path) or not path:
                    for x in INDEXFILE:
                        tmp = filepath.join(path, x)
                        dprint(tmp)
                        if filepath.isfile(tmp):
                            responseText = open(tmp, encoding="utf-8").read()
        
                            # ヘッダー作成
                            self.send_response(200, "OK")
                            self.send_header("Content-type", "text/html; charset=utf-8")
                            # responseText の byte変換
                            byteResponce = bytes(responseText, encoding="utf-8")
                            break


                    else: # auto index is not found
                        # response header
                        dprint(f"index not found super:{self.path}")
                        return super().do_GET()


            # 存在しないpathの場合 405 で Not Found と表示 <- なぜか404ではないが とりあえず要件道理に
            else:
                responseText = "Not found"

                # ヘッダー作成
                self.send_response(405, "Not found")
                self.send_header("Content-type", "text/html; charset=utf-8")
                # responseText の byte変換
                byteResponce = bytes(responseText, encoding="utf-8")


            # 出力
            # response送信
            self.end_headers()
            # データ送信
            self.wfile.write(byteResponce)


        # serverを隠す
        def send_response(self, code, message=None):
            self.log_request(code)
            self.send_response_only(code, message)
            #self.send_header('Server', self.version_string())
            self.send_header('Date', self.date_time_string())

        #ROOTDIRECTORY を固定
        def __init__(self, *args, directory=None, **kwargs):

            super().__init__(*args, directory=ROOTDIRECTORY, **kwargs)



    def main():
        # インスタンス
        server = HTTPServer(
            server_address = (BIND_IP, BIND_PORT),
            RequestHandlerClass = CustomHandler
            )

        # 起動
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("stop server")



    if __name__ == "__main__":
        print(main())
