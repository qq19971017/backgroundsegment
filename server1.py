from socket import *
import json
import time

HOST = ''
PORT = 6688
BUFSIZE = 4096
ADDR = (HOST, PORT)

# car = {'Position':0, 'CarArrived':False, 'ResetCarPosition':False, 'CarPatrol':False}
# data1 = json.dumps(car)

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen(10)


print('waiting for connection...')
tcpClient, addr = tcpServer.accept()
print(addr)

while 1:

    data = tcpClient.recv(BUFSIZE)

    if data:
        car_recv = data.decode()
        data_exchange = json.loads(car_recv)
        if data_exchange['ResetCarPosition'] == True:

            print("["+time.ctime()+"]"  + "异常解除，巡逻车归位")
            time.sleep(3)
            print("["+time.ctime()+"]"  +"巡逻车已归位,准备就绪")
            data_exchange['CarPatrol'] = True
            data = json.dumps(data_exchange)

            tcpClient.send(data.encode())


        elif data_exchange['Position']>=0 and data_exchange['CarArrived'] == False:
            print("["+time.ctime()+"]"  +"异常发生，巡逻车前往位置：" + str(data_exchange['Position']))
            time.sleep(3)
            print("["+time.ctime()+"]"  +"小车到达")
            data_exchange['CarArrived'] =True
            data = json.dumps(data_exchange)
            tcpClient.send(data.encode())

tcpClient.close()
tcpServer.close()