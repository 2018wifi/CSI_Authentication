# Public
DEBUG = True # 调试模式开关
BW = 20  # 带宽
NFFT = int(BW * 3.2)
PCAP_SIZE = 100  # 每个pcap包含的CSI数组个数


# get_fingerprint
RATE = 50           # 发包速率，单位：包/秒
SERVER_IP = '192.168.0.101'         # TODO:删掉并将ServerIp改为实时的
NEW_DEVICE_PORT = 8000
BYTE_NUM = 500      # 发送内容的字节长度(0...1472)

RASP_NUM = 2                    # 树莓派数量
RASP_IP1 = "192.168.0.104"
RASP_IP2 = "192.168.0.105"
RASP_IP3 = "192.168.0.106"
PORT1 = 9600
PORT2 = 9601
PORT3 = 9602
DATE_DELTA = 1589469244167      # 时间戳会是相对这个时间的间隔，避免太长无法放入numpy数组


# detect
MODEL_PATH = 'model.pkl'


# plot
LENGTH = 10
WIDTH = 10
POS = [(1., 2.), (5., 3.), (6., 9.)]


# model
T_NUM = 3 # 位置数量
T_SIZE = 50 # 每个位置的包的数量
LOAD_EXISTING_DATA = True
SAVE_DATA = True
INPUT_SIZE = PCAP_SIZE * NFFT
VAL_SIZE = 50
HIDDEN_WIDTH = 50
OUTPUT_SIZE = T_NUM
epochs = 5000
learning_rate = 1e-2
dynamically_adjust = False
