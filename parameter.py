# Public
DEBUG = True            # 调试模式开关
BW = 20                 # 带宽
NFFT = int(BW * 3.2)
FP_SIZE = 150           # 指纹长度


# get_fingerprint
RATE = 50                       # 发包速率，单位：包/秒
NEW_DEVICE_PORT = 8000
BYTE_NUM = 500                  # 发送内容的字节长度(0...1472)

TARGET_IP = "192.168.0.101"             # 目标设备IP
TARGET_MAC = "DC:08:0F:26:6E:1D"        # 目标设备MAC

RASP_COUNT = 3                  # 树莓派数量
RASP_STATE1 = True              # 树莓派状态
RASP_STATE2 = True
RASP_STATE3 = True
RASP_IP1 = "192.168.0.104"      # 树莓派IP
RASP_IP2 = "192.168.0.105"
RASP_IP3 = "192.168.0.103"
RASP_PORT = 9600                # 树莓派接收指纹请求的端口
SERVER_PORT = 9605              # 主机接收树莓派提示新主机连接信息的端口
SERVER_PORT1 = 9600             # 主机接收CSI的端口
SERVER_PORT2 = 9601
SERVER_PORT3 = 9602

MAX_SEND_UDP_TIME = 10                    # 发送UDP的持续时间（相当于超时时间）


# CNN_pytorch
NPY_SIZE = 150                 # 每个npy包含的CSI数组个数


# model
T_NUM = 9 # 位置数量
T_SIZE = 50 # 每个位置的包的数量
LOAD_EXISTING_DATA = False
SAVE_DATA = True
INPUT_SIZE = FP_SIZE * NFFT
VAL_SIZE = 50                   # VAL_SIZE is validation size
HIDDEN_WIDTH = 50               # HIDDEN_WIDTH is the width of hidden dimension; OUTPUT_SIZE is output dimension;
OUTPUT_SIZE = T_NUM
epochs = 5000
learning_rate = 1e-2
dynamically_adjust = False
