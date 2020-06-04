"""
client.py
encode()/decode()
"""
from socket import *
import json

HOST = 'localhost'
PORT = 11113
BUFSIZE = 4096
ADDR = (HOST, PORT)

tcpClient = socket(AF_INET, SOCK_STREAM)
tcpClient.connect(ADDR)



while 1:
    data = input('> ')

    if not data:
        break
    tcpClient.send(data.encode())

    data = tcpClient.recv(BUFSIZE)
    print(data.decode())
    if not data:
        break

tcpClient.close()
