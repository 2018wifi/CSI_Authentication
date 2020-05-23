# Public
BW = 20  # 带宽
NFFT = int(BW * 3.2)
PCAP_SIZE = 100  # 每个pcap包含的CSI数组个数

VAL_SIZE = 150

# CNN_pytorch
LOAD_EXISTING_DATA = False
SAVE_DATA = True
HIDDEN_WIDTH = 50
epochs = 5000
learning_rate = 1e-2
dynamically_adjust = False

# cluster_sklearn.py
N_CLUSTERS = 7
