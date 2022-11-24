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
#

from ipaddress import ip_address
from os.path import isdir, abspath, exists, dirname
from os import getcwd


class easyWebserver(object):
    class IPAddrError(ValueError):pass
    class PortError(ValueError):pass
    class DirectoryError(NotADirectoryError):pass

    def __init__(self):
        self.__server = None
        self.refresh()

    # Reset to initialize state
    def refresh(self):
        self.setIp("0.0.0.0")
        self.setPort(8080)
        self.setDocRoot(getcwd())
        self.closeServer()

    # ip set/get
    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.setIp(value)
        return self.ip

    def getIp(self):
        return self.__ip

    def setIp(self, ip) -> None:
        try:
            IP = ip_address(ip)
            if not f"{IP}" in self.ipScan():
                raise ValueError

        except ValueError:
            raise easyWebserver.IPAddrError("this IP has not been assigned to computer")

        self.__ip = IP

    # port set/get
    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.setPort(value)
        return self.port

    def getPort(self):
        return self.__port

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
    def docRoot(self):
        return self.__docRoot

    @docRoot.setter
    def docRoot(self, value):
        self.setDocRoot(value)
        return self.docRoot

    def getDocRoot(self):
        return self.__docRoot

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
        from socket import gethostname, gethostbyname_ex
        return (*gethostbyname_ex(gethostname())[2], "0.0.0.0", "127.0.0.1")


    def openServer(self):
        if not self.is_openServer():
            try:
                from threading import Thread
                from ftpserver import serverSaving
                self.__server = serverSaving(str(self.ip), self.port, self.docRoot)
                Thread(target=self.__server.serve_forever, daemon=True).start()
            except:
                self.closeServer()

    def closeServer(self):
        if self.__server is not None:
            self.__server.shutdown()
            self.__server.__exit__()
            self.__server = None

    def is_openServer(self):
        return self.__server is not None

    def showValue(self):
        return {"ip":self.ip,"port":self.port,"directory":self.docRoot}


    def __setattr__(self, key, value):
        tmp = key.rpartition("__")
        tmp = tmp[0]+tmp[1], tmp[2]
        # 書き込み許可を絞る
        # x は変数名を表す
        # self.x はオーバーライドできる変数 self.__x はそのクラス固有の変数
        if (not tmp[0] or (tmp[0]=="_easyWebserver__") # self.x か self.__x のみ許可
            ) and (tmp[1] in ("docRoot", "ip", "port") # 特定の変数名のみ許可
            ) or self.__class__.__base__.__name__ != "object" or key=="_easyWebserver__server": # オーバーライドされたら全許可
            return object.__setattr__(self, key, value)
        error = f"Could not access '{key}'. Not Authorized"
        raise AttributeError(error)


if __name__ == "__main__":
    class a(easyWebserver):
        def ass(self):
            self.port = 888
            self.__ip = "0.0.8.0"
            print(self.showValue())

    aaa = easyWebserver()
    aaa.ip = "0.0.0.0"
    aaa.port = 8080
    aaa.docRoot = "./"
    try:
        aaa.openServer()
        input("server opend....eney key stoped>_")
    finally:
        aaa.closeServer()
        input("server stoped....")
    a().ass()
