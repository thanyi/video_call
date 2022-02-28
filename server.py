from websocket_server import WebsocketServer
import threading
import cv2
import base64
import time
import json
'''
这是个关于websocket的前后端框架，是在websocket的server框架上面进行了修改

目的是为了进行指定端对端的视频传输
'''
camera1 = None
# frame = cv2.imread("1.jpg", cv2.IMREAD_COLOR)
rtsp_path = 0

videoConnTable = {}
pairTable = {}


# Called for every client connecting (after handshake)
def new_client(client, server):
    '''
    用来进行框架中
        有新的client链接
            的事件处理函数
    :param client:
    :param server:
    :return:
    '''
    print("New client connected and was given id %d" % client['id'])
    message = {"id": client["id"]}
    server.send_message(client, json.dumps(message))
    # 发送给所有的连接
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    '''
    用来进行框架中
        有新的client离开
            的事件处理函数
    :param client:
    :param server:
    :return:
    '''
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    '''
    用来进行框架中
        消息接收和消息发送
            的事件处理函数
    :param client:
    :param server:
    :return:
    '''
    if len(message) > 200:
        message = message[:200] + '..'
    print("Client(%d) said: %s" % (client['id'], message))
    global camera1
    camera1 = cv2.VideoCapture(message)


# 发送给所有的连接
# server.send_message_to_all(message)
def from_vedio():

    thread1 = threading.Thread(target=vedio_thread1, args=(1,))
    #     thread1.setDaemon(True)
    thread1.start()
    thread2 = threading.Thread(target=vedio_thread2, args=(1,))
    #     thread1.setDaemon(True)
    thread2.start()
    print('start')


def vedio_thread1(n):
    print('send')
    while True:
        if len(server.clients) > 0:
            image = cv2.imencode('.jpg', frame)[1]
            base64_data = base64.b64encode(image)
            s = base64_data.decode()
            # print('data:image/jpeg;base64,%s'%s)
            # print(server.clients)
            message = {}
            message["img"] = "data:image/jpeg;base64,%s" % s
            server.send_message_to_all(json.dumps(message))
        time.sleep(0.05)


def vedio_thread2(n):
    global camera1
    camera1 = cv2.VideoCapture(rtsp_path)
    global frame
    while True:
        _, img_bgr = camera1.read()
        if img_bgr is None:
            camera1 = cv2.VideoCapture(rtsp_path)
            print('丢失帧')
        else:
            frame = img_bgr


# Server Port
PORT = 8124
# 创建Websocket Server
server = WebsocketServer("192.168.43.70", PORT)
from_vedio()
# 有设备连接上了
server.set_fn_new_client(new_client)
# 断开连接
server.set_fn_client_left(client_left)
# 接收到信息
server.set_fn_message_received(message_received)
# 开始监听
server.run_forever()
