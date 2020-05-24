import os
import sys
import socket
import threading

SERVER_IP = "192.168.0.100"
SERVER_PORT = 9605                      # 新连接信息发往主机的端口
SERVER_CSI_PORT = 9600                  # CSI信息发往主机的端口

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
        r_v = os.system("./detectConnection.sh")
        connected_devices_temp = []
        with open("./tmp.txt", 'r') as f:
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
    # tcp_socket.close()

def send_csi(count):
    while True:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(("", SERVER_PORT))
        tcp_socket.listen(128)
        print("等待主机请求指纹...")
        reply = "OK"

        client_socket, client_addr = tcp_socket.accept()

        mes = client_socket.recv(4096)
        target_mac, count = mes.split()[0], mes.split()[1]
        print("准备传送MAC: ", target_mac, "的", count, "个包")
        client_socket.send(reply.encode())
        client_socket.close()
        tcp_socket.close()

        p = os.popen("mcp -c 1/20 -C 1 -N 1 -m" + str(target_mac), 'r', 1)
        os.system("nexutil -Iwlan0 -s500 -b -l34 -v" + p.read())
        os.system("./middleman " + str(SERVER_CSI_PORT) + " " + str(count))


if __name__ == '__main__':
    detector = threading.Thread(target=detect_new_connection())
    detector.start()                # 只需要一个树莓派调用了此函数即可
    send_csi()                      # 等待请求指纹并发送CSI


