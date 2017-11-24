#coding=utf-8

import socket
from urllib.parse import urlparse
from optparse import OptionParser

'''
python 3 ms15-034_check
'''

def get_ms15_034(host,port):
    # if ipAddr.startswith("http"):
    #     host=urlparse(ipAddr).netloc
    #     port=80
    # elif ipAddr.startswith("https"):
    #     host=urlparse(ipAddr).netloc
    #     port=443
    # else:
    #     host=ipAddr
    #     port=port
    # print(host,port)
    hexAllFfff = "18446744073709551615"
    vulns = ("GET / HTTP/1.1\r\nHost: %s\r\nRange: bytes=0-" + hexAllFfff + "\r\n\r\n")%host
    vulns=vulns.encode('ascii')
    print ("[*] Audit Started")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host,port))
    c.sendall(vulns)
    resp = c.recv(1024)
    print('resp=',resp.decode("utf-8"))

    if ("microsoft".encode('ascii')  in resp) or ('IIS'.encode('ascii') in resp) : 
        print ("[+]服务器是IIS")
        c.close()            
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((host, port))
        c.send(vulns)
        result= c.recv(1024)
        print('result=??',result)
        if "Requested Range Not Satisfiable".encode('ascii') in result:
            print ("[!!]存在MS15-034风险。修复方案，更新补丁KB3042553。")
        elif "The request has an invalid header name".encode('ascii') in result:
            print ("[*] 已安装补丁")
        else:
            print ("[*] 异常响应无法判断补丁是否安装")
    else:
        print ("[*]服务器不是IIS")
        c.close()
        exit(0)

if __name__=='__main__':
    parse=OptionParser()
    parse.add_option("-H","--host",type="string",help='IP or domain')
    parse.add_option("-P","--port",action="store",default=80,type="int",help='Port,default port is 80')
    (options,args)=parse.parse_args()
    if options.host:
        get_ms15_034(options.host,options.port)
    else:
        print('parameters not enough')

