import socket
from parameter import *
from get_fingerprint import get_fingerprint
from detect import detect
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


if __name__ == '__main__':
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", SERVER_PORT))
    tcp_socket.listen(128)
    print("等待主树莓派连接")

    client_socket, client_addr = tcp_socket.accept()
    print("主树莓派连接成功")

    while True:
        mes = client_socket.recv(4096)
        TARGET_IP, TARGET_MAC = mes.split()
        print("提示：有新主机连接入局域网中\tIP: ", TARGET_IP, "\tMAC: ", TARGET_MAC)
        matrix = get_fingerprint()
        isInvade = detect(matrix)

        if isInvade:
            print("WARNING: IP: {0}\tMAC: {1}认证失败！".format(TARGET_IP, TARGET_MAC))
            lena = mpimg.imread('./assets/WARNING.png')

            plt.imshow(lena)
            plt.axis("off")
            plt.show()

            # 在此也可以给远程主机发送警告
        else:
            with open("./temp/last_fingerprint.npy", 'wb'):
                pass
            np.save("./temp/last_fingerprint.npy", matrix)
            print("新主机认证成功")

    # tcp_socket.close()

