"""
server.py
encode()/decode()
"""
from socket import *
from time import ctime

HOST = ''
PORT = 11113
BUFSIZE = 4096
ADDR = (HOST, PORT)

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen(10)

while 1:
    print('waiting for connection...')
    tcpClient, addr = tcpServer.accept()
    print(addr)

    while 1:
        data = tcpClient.recv(BUFSIZE)
        print(data.decode())

        if not data:
            print('---------')
            break;

        buf = '[' + ctime() + ']' + data.decode()
        tcpClient.send(buf.encode())

    tcpClient.close()
tcpServer.close()

# class dataExchange:
#
#
#     Position=0
#     CarArrived =False
#     ResetCarPosition = False
#     CARPATROL = False
#
#     def __init__(self, Position, CarArrived, ResetCarPosition,CARPATROL ):
