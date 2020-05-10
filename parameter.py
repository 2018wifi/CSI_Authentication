# Public
DEBUG = True # 调试模式开关
BW = 20  # 带宽
NFFT = int(BW * 3.2)
PCAP_SIZE = 3 * 50  # 每个pcap包含的CSI数组个数


# get_data



# process
MODEL_PATH = 'model.pkl'


# model
T_NUM = 6 # 位置数量
T_SIZE = 70 # 每个位置的包的数量
LOAD_EXISTING_DATA = True
SAVE_DATA = True
INPUT_SIZE = PCAP_SIZE * NFFT
VAL_SIZE = 50
HIDDEN_WIDTH = 50
OUTPUT_SIZE = T_NUM
epochs = 5000
learning_rate = 1e-2
dynamically_adjust = False
