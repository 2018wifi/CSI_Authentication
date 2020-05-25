from get_fingerprint import get_fingerprint
from parameter import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

print("提示：有新主机连接入局域网中\tIP: ", TARGET_IP, "\tMAC: ", TARGET_MAC)
lena = mpimg.imread('./assets/WARNING.png')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(5, 5))
fig.canvas.set_window_title('警告！')
plt.imshow(lena)
plt.axis('off')
plt.title("IP:{0}   MAC:{1}认证失败！\n".format(TARGET_IP, TARGET_MAC))
plt.show()
