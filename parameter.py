# Public
DEBUG = True # 调试模式开关
BW = 20  # 带宽
NFFT = int(BW * 3.2)
FP_SIZE = 150  # 指纹长度


# get_fingerprint
RATE = 50           # 发包速率，单位：包/秒
SERVER_IP = '192.168.0.101'         # TODO:删掉并将ServerIp改为实时的
NEW_DEVICE_PORT = 8000
BYTE_NUM = 500      # 发送内容的字节长度(0...1472)

TARGET_IP = None                # 目标设备IP
TARGET_MAC = None               # 目标设备MAC

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

TIMEOUT = 60                    # 树莓派发送超时时间


# model
T_NUM = 3 # 位置数量
T_SIZE = 50 # 每个位置的包的数量
LOAD_EXISTING_DATA = True
SAVE_DATA = True
INPUT_SIZE = FP_SIZE * NFFT
VAL_SIZE = 50
HIDDEN_WIDTH = 50
OUTPUT_SIZE = T_NUM
epochs = 5000
learning_rate = 1e-2
dynamically_adjust = False
