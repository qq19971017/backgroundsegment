from socket import *
import json
import time
import select

HOST = 'localhost'
PORT = 6688
BUFSIZE = 4096
ADDR = (HOST, PORT)

tcpClient = socket(AF_INET, SOCK_STREAM)

tcpClient.connect(ADDR)

input = [tcpClient]
# tcpClient.setblocking(False)
print("["+time.ctime()+"]"  +"发现异常")
data_exchange = {'Position':0, 'CarArrived':False, 'ResetCarPosition':False, 'CarPatrol':False}
data = json.dumps(data_exchange)
tcpClient.send(data.encode())
tcpClient.settimeout(5)

while 1:
    rs, ws, es = select.select(input, [], [], 1)
    for indata in rs:
        if indata == tcpClient:
            data = tcpClient.recv(BUFSIZE)
            if data:
                car_recv = data.decode()
                data_exchange = json.loads(car_recv)
                if data_exchange['CarPatrol'] == True:
                    print("["+time.ctime()+"]"  +"小车已经就绪，重置实验")
                    data_exchange = {'Position':0, 'CarArrived':False, 'ResetCarPosition':False, 'CarPatrol':False}
                elif data_exchange['CarArrived'] == True:
                    print("["+time.ctime()+"]"  +"小车已经到达异常点，开始处理异常")
                    time.sleep(3)
                    print("["+time.ctime()+"]"  +"处理异常结束，小车归位")
                    data_exchange['ResetCarPosition'] = True
                    data = json.dumps(data_exchange)
                    tcpClient.send(data.encode())
    print("1")


tcpClient.close()