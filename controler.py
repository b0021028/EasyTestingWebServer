#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# controler
'''*1
Belongs : YIC 情報ビジネス専門学校 情報工学科 2年
Name    : 山崎 晃弘 
E-Mail  : B0021028@ib.yic.ac.jp
'''
#
#
#

from ipaddress import ip_address
from os.path import isdir, abspath, exists, dirname
from os import getcwd

from socket import gethostname, gethostbyname_ex
from threading import Thread
from _server import getHttpServer


class easyWebserver(object):
    class IPAddrError(ValueError):pass
    class PortError(ValueError):pass
    class DirectoryError(NotADirectoryError):pass

    __server = None

    def __init__(self, ip=None,port=None,directory=None):
        print(self.__server)
        self.refresh()
        if ip:
            self.ip = ip
        if port:
            self.port = port
        if directory:
            self.docRoot = directory

    # Reset to initialize state
    def refresh(self):
        self.setIp("0.0.0.0")
        self.setPort(8080)
        self.setDocRoot(getcwd())
        self.closeServer()

    # ip set/get
    @property
    def ip(self): return self.__ip

    @ip.setter
    def ip(self, value):
        self.setIp(value)
        return self.ip

    def getIp(self): return self.__ip

    def setIp(self, ip) -> None:
        try:
            IP = ip_address(ip)
            if not (IP.is_loopback or f"{IP}" in self.ipScan()):
                raise ValueError

        except ValueError:
            raise easyWebserver.IPAddrError("this IP has not been assigned to computer")

        self.__ip = IP

    # port set/get
    @property
    def port(self): return self.__port

    @port.setter
    def port(self, value):
        self.setPort(value)
        return self.port

    def getPort(self): return self.__port

    def setPort(self, port) -> None:
        try:
            PORT = int(port)
            if not ((0 < PORT < 65536) and f"{PORT}" == f"{port}"):
                raise ValueError

        except ValueError:
            raise easyWebserver.PortError("It is Bat Port.")

        self.__port = PORT


    # dir set/get
    @property
    def docRoot(self): return self.__docRoot

    @docRoot.setter
    def docRoot(self, value):
        self.setDocRoot(value)
        return self.docRoot

    def getDocRoot(self): return self.__docRoot

    def setDocRoot(self, docRoot) -> None:
        try:
            if not exists(docRoot):
                raise NotADirectoryError

            elif not isdir(docRoot):
                docRoot = dirname(docRoot)

            DOCROOT = abspath(docRoot)

        except NotADirectoryError:
            raise easyWebserver.DirectoryError("It is Bat Directory Path.")

        self.__docRoot = DOCROOT


    def ipScan(self) -> tuple[str,...]:
        return (*gethostbyname_ex(gethostname())[2], "0.0.0.0", "127.0.0.1")


    def openServer(self):
        if not self.is_openServer():
            try:
                self.__server = getHttpServer(str(self.ip), self.port, self.docRoot)
                t=Thread(target=self.__server.serve_forever, daemon=True)
                t.start()
            except Exception as e:
                self.closeServer()
                raise e

    def closeServer(self):
        if self.__server is not None:
            self.__server.shutdown()
            self.__server.__exit__()
            self.__server = None

    def is_openServer(self):
        return self.__server is not None

    def showValue(self):
        return {"ip":self.ip,"port":self.port,"directory":self.docRoot}

    def __dict__(self):
        return {"ip":self.ip,"port":self.port,"directory":self.docRoot}


    def __setattr__(self, key, value):
        tmp = key.rpartition("__")
        tmp = tmp[0]+tmp[1], tmp[2]
        # 書き込み許可を絞る
        # x は変数名を表す
        # 基礎知識メモ::self.x はオーバーライドできる変数 self.__x はそのクラス固有の変数
        if ((
            (not tmp[0]) or (tmp[0]=="_easyWebserver__") # self.x か self.__x のみかつ、
            ) and (
                tmp[1] in ("docRoot", "ip", "port")# 、特定の変数名のみ許可
            )) or (
             key=="_easyWebserver__server" # 指定して許可 self.__x
            ) or self.__class__.__base__.__name__ != "object" : # オーバーライドされたら全許可
            return object.__setattr__(self, key, value)
        error = f"Could not access '{key}'. Not Authorized"
        raise AttributeError(error)


if __name__ == "__main__":
    import argparse
    from ipaddress import ip_address
    from os.path import isdir

    def ip(x):
        return str(ip_address(x))
    def port(x):
        _x = int(x)
        if not (0 < _x < 0x10000):raise ValueError
        return _x
    def directory(x):
        _x = str(x)
        if not isdir(_x):raise ValueError
        return _x

    argsPars = argparse.ArgumentParser()    
    argsPars.add_argument('-i', '--ip', "--ipaddress",  dest='ip',        type=ip,        default=argparse.SUPPRESS, metavar="IP",        help='set binding ip address')
    argsPars.add_argument('-p', '--port',               dest='port',      type=port,      default=argparse.SUPPRESS, metavar="PORT",      help='set binding port')
    argsPars.add_argument('-d', '--dir', '--directory', dest='directory', type=directory, default=argparse.SUPPRESS, metavar="DIRECTORY", help='set web server root directory')
    #argsPars.add_argument('--start', '-s', help='set binding port', action='store_true')
    #default="0.0.0.0", default=8080, default="./",

    argsPars = dict(argsPars.parse_args()._get_kwargs())
    argsPars["ip"] = "::1"
    print(argsPars)

    if not "test":
        class testOverride(easyWebserver):
            def addmethod(self):
                self.port = 888 # effect
                self.__ip = "0.0.8.0" # no effect
                print(self.showValue())
        testOverride().addmethod()


    aaa = easyWebserver(**argsPars)

    try:
        aaa.openServer()
        input("server opend....eney key stoped>_")
    finally:
        aaa.closeServer()
        print("server stoped....")
