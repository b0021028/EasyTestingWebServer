###!/usr/bin/python
#-*- coding: utf-8 -*-
#
# server class
'''*1
Belongs : YIC 情報ビジネス専門学校 情報工学科 2年
Name    : 山崎 晃弘 
E-Mail  : B0021028@ib.yic.ac.jp
'''
#
#

from http.server import (
    SimpleHTTPRequestHandler,
    ThreadingHTTPServer as _ThreadingHTTPServer,
    CGIHTTPRequestHandler as _CGIHTTPRequestHandler
)
from os.path import (
    join as osPathJoin,
    exists as osPathExists
)
#from sys import version_info
#SYSVERCHECK = version_info >= (3,10)
#del version_info
#if not SYSVERCHECK:
#    from typing import Union




# path と query と fragment を切り分ける
def splitURN(pathAndQuery="/") -> tuple[str,str,str]:
    """* `"/example/top.html?q=testserch&ab;c#t1"` -> `("/example/top.html", "q=testserch&ab;c", "t1")`\n\n* urn -> (path , query(?) , fragment(#))"""
    path, _, fragment = str(pathAndQuery).partition("#")
    path, _, query = path.partition("?")
    if fragment:
        print(RuntimeWarning(RuntimeError(f"Why coul'd getting 'url fragment'? fragment:{fragment}")))

    return (path, query, fragment)


#from urllib.parse import unquote
## URLデコーダー
#def decodeURL(txt):
#    return unquote(txt)




class CGIHTTPRequestHandler(_CGIHTTPRequestHandler):
#    protocol_version = "HTTP/1.1"
    protocol_version = "HTTP/1.0"
    cgi_directories = []
    sys_version = ""
    server_version = "Easy Web Server"

    def is_cgi(self):
        filename = splitURN(self.path)[0].rpartition("/")
        #print(filename, self.path, sep=" [@] ")
        if filename[-1].rpartition(".cgi.py")[0]:
            self.cgi_info = (filename[0::2])
            return True

        return False

    def send_head(self):
        filename = splitURN(self.path)[0]
        for index in "index.html", "index.htm", "index.cgi.py":
            index = osPathJoin(filename, index)
            if osPathExists(index):
                path = index
                break

        if self.is_cgi():
            return self.run_cgi()

        else:
            return SimpleHTTPRequestHandler.send_head(self)


class ThreadingHTTPServer(_ThreadingHTTPServer):
    address_family = 2

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass, bind_and_activate: bool = ..., rootDir:str=None) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.__docRoot_dir = rootDir

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(
            request, client_address, self,
            directory=self.__docRoot_dir
            )
        #self.close_request(request)





def getHttpServer(ip:str="0.0.0.0", port:int=8080, dir:str=None):
    return ThreadingHTTPServer((ip, port), CGIHTTPRequestHandler, rootDir=dir)

