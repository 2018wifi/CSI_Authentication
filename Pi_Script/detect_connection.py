import os
import time
import socket
import threading

SERVER_IP = "192.168.0.100"
SERVER_PORT = 9605                      # 新连接信息发往主机的端口
DETECT_INTERVAL = 30                    # 检测时间间隔，单位: s

class Connection:                       # 局域网内的连接
    def __init__(self, ip, mac):
        self.IP = ip
        self.MAC = mac


def detect_new_connection():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ip = SERVER_IP
    tcp_port = SERVER_PORT
    tcp_socket.connect((tcp_ip, tcp_port))

    connected_devices = []

    while True:
        os.system("./detectConnection.sh")
        connected_devices_temp = []
        with open("./ipmac.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                ip, mac = line.split()
                connected_devices_temp.append(Connection(ip, mac))
        for item in connected_devices_temp:
            if item not in connected_devices:
                mes = item.IP + " " + item.MAC
                tcp_socket.send(mes.encode())
                print("发现并已提示有新主机连接: IP", item.IP, "\tMAC: ", item.MAC)
        connected_devices = connected_devices_temp
        time.sleep(DETECT_INTERVAL)
    # tcp_socket.close()


if __name__ == '__main__':
    detect_new_connection()