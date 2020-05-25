# -*- coding: UTF-8 -*-
import os
import sys
import socket
import threading

SERVER_CSI_PORT = 9600                  # CSI信息发往主机的端口
RASP_PORT = 9600                        # CSI接收主机CSI请求端口


def send_csi():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", RASP_PORT))
    tcp_socket.listen(128)
    print("等待主机请求指纹...")
    reply = "OK"
    while True:
        client_socket, client_addr = tcp_socket.accept()

        mes = client_socket.recv(4096).decode()
        temp = mes.split()
        target_mac, count = temp[0], temp[1]
        print("准备传送MAC: ", target_mac, "的", count, "个包")
        client_socket.send(reply.encode())
        client_socket.close()

        p = os.popen("mcp -c 1/20 -C 1 -N 1 -m " + target_mac)
        mcp = p.read()
        os.popen("nexutil -Iwlan0 -s500 -b -l34 -v" + mcp)
        os.popen("./middleman " + str(SERVER_CSI_PORT) + " " + str(int(count) * 2))      # 这里要求middleman发送两倍的数据，以确保对面收到足够的数据
        print("CSI向量发送完毕")
    # tcp_socket.close()


if __name__ == '__main__':
    sender = threading.Thread(target=send_csi())  # 等待请求指纹并发送CSI
    sender.start()
    detector = threading.Thread(target=detect_new_connection())  # 只需要一个树莓派调用了此函数即可
    detector.start()


