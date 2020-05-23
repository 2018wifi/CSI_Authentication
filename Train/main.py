import tensorflow as tf
from tensorflow import keras
import numpy as np

BW = 20  # 带宽
NFFT = int(BW * 3.2)
GESTURE_NUM = 3  # 手势数
TRAIN_SIZE = 210  # 训练集大小
PCAP_SIZE = 100  # 每个pcap包含的CSI数组个数

train_data = np.zeros((TRAIN_SIZE, PCAP_SIZE, NFFT))
train_result = np.zeros(TRAIN_SIZE)

for i in range(1, 70 + 1):
    # 读取npy文件
    temp_T1 = np.load('data/T1/T1_' + str(i) + '.npy')
    temp_T2 = np.load('data/T2/T2_' + str(i) + '.npy')
    temp_T3 = np.load('data/T3/T3_' + str(i) + '.npy')

    # CSI求模&&毛刺处理
    for j in range(PCAP_SIZE):
        for k in range(NFFT):
            temp_T1[j][k] = abs(temp_T1[j][k])
            temp_T2[j][k] = abs(temp_T2[j][k])
            temp_T3[j][k] = abs(temp_T3[j][k])
            if k == 0 or k == 29 or k == 30 or k == 31 or k == 32 or k == 33 or k == 34 or k == 35:
                temp_T1[j][k] = 0
                temp_T2[j][k] = 0
                temp_T3[j][k] = 0

    # 加入学习队列
    temp_T1 = temp_T1.astype('float64')
    temp_T2 = temp_T2.astype('float64')
    temp_T3 = temp_T3.astype('float64')
    train_data[i - 1] = temp_T1[0:PCAP_SIZE, :]
    train_data[70 + i - 1] = temp_T2[0:PCAP_SIZE, :]
    train_data[140 + i - 1] = temp_T3[0:PCAP_SIZE, :]
    train_result[i - 1] = 0
    train_result[70 + i - 1] = 1
    train_result[140 + i - 1] = 2

# 训练数据归一化
cnt = 0
for i in range(TRAIN_SIZE):
    for j in range(PCAP_SIZE):
        #print(train_data[i][j])
        CSI_max = train_data[i][j].max()
        if CSI_max == 0:
            cnt = cnt + 1
        for k in range(NFFT):
            # if train_data[i][j][k] == 0:
            #     train_data[i][j][k] = 1
            train_data[i][j][k] = train_data[i][j][k]/CSI_max
print(str(cnt))

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(PCAP_SIZE, NFFT)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(GESTURE_NUM)
])
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
model.fit(train_data, train_result, validation_split=0.1, epochs=10)


