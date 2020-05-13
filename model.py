from parameter import *

import torch
import torch.nn as nn
import torch.nn.functional as functional
import numpy as np
import random
import os
import torch.optim.lr_scheduler as lr_scheduler


if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')


class Net(torch.nn.Module):
    def __init__(self, HEIGH, WIDTH, OUTPUT_SIZE):
        super(Net, self).__init__()
        self.HEIGH = HEIGH
        self.WIDTH = WIDTH
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * ((((HEIGH-4)//2)-4)//2) * ((((WIDTH-4)//2)-4)//2), 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, OUTPUT_SIZE)
        self.dropout = torch.nn.Dropout(p=0.2)
        # self.linear1 = torch.nn.Linear(INPUT_SIZE, HIDDEN_WIDTH)
        # self.linear2 = torch.nn.Linear(HIDDEN_WIDTH, HIDDEN_WIDTH)
        # self.linear3 = torch.nn.Linear(HIDDEN_WIDTH, OUTPUT_SIZE)


    def forward(self, x):
        x = self.pool(functional.relu(self.conv1(x)))
        x = self.pool(functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * ((((self.HEIGH-4)//2)-4)//2) * ((((self.WIDTH-4)//2)-4)//2))
        x = self.dropout(functional.relu(self.fc1(x)))
        x = self.dropout(functional.relu(self.fc2(x)))
        x = self.fc3(x)
        return x
        # # use dropout() to prevent over learning
        # x = self.dropout(functional.relu(self.linear1(x)))
        # x = self.dropout(functional.relu(self.linear2(x)))
        # # the output dimension shouldn't use dropout()
        # y_pred = functional.softmax(self.linear3(x), dim=1)
        # return y_pred

if __name__ == '__main__':
    print(device)
    if LOAD_EXISTING_DATA:
        x = torch.load('data_x.pt').to(device)
        y = torch.load('data_y.pt').to(device)
    else:
        x = torch.zeros((T_NUM * T_SIZE, PCAP_SIZE, NFFT), device=device)
        y = torch.zeros((T_NUM * T_SIZE, OUTPUT_SIZE), device=device)
        cnt = 0
        for i in range(T_NUM):
            for j in range(T_SIZE):
                temp_y = torch.zeros(T_NUM)
                temp_y[i] = 1
                # read .npy file
                file = 'data/T' + str(i+1) + '/T' + str(i+1) + '_' + str(j+1) + '.npy'
                temp_x = np.load(file)
                for k in range(PCAP_SIZE):
                    temp_x[k] = abs(temp_x[k])
                temp_x = torch.from_numpy(temp_x.astype('float64'))[0:PCAP_SIZE]
                # clean and normalize data
                for k in [0, 29, 30, 31, 32, 33, 34, 35]:
                    temp_x[:, k] = 0
                for k in range(temp_x.shape[0]):
                    CSI_max = temp_x[k].max()
                    for p in range(temp_x.shape[1]):
                        temp_x[k][p] = temp_x[k][p] / CSI_max
                # concatenates to x and y
                x[cnt] = temp_x
                y[cnt] = temp_y
                cnt += 1
                print(i, j)
    if SAVE_DATA:
        torch.save(x, 'data_x.pt')
        torch.save(y, 'data_y.pt')
    # Extract test batch
    x = torch.reshape(x, (T_SIZE*T_NUM, 1, PCAP_SIZE, NFFT))
    test_x = torch.zeros((VAL_SIZE, PCAP_SIZE, NFFT), device=device)
    test_y = torch.zeros((VAL_SIZE, OUTPUT_SIZE), device=device)
    for i in range(VAL_SIZE):
        n = random.randint(0, x.shape[0] - 1)
        # print(n)
        test_x[i] = x[n]
        test_y[i] = y[n]
        x = torch.cat((x[:n], x[n+1:]))
        y = torch.cat((y[:n], y[n+1:]))
    test_x = torch.reshape(test_x, (VAL_SIZE, 1, PCAP_SIZE, NFFT))
    x.requires_grad = True
    y.requires_grad = True
    # Construct our model by instantiating the class defined above
    model = Net(PCAP_SIZE, NFFT, OUTPUT_SIZE).to(device)

    # Construct a loss function and an Optimizer. The call to model.parameters()
    # in the SGD constructor will contain the learnable parameters of the two
    # nn.Linear modules which are members of the model.
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, 'min')
    for t in range(epochs):
        optimizer.zero_grad()
        # Forward pass: Compute predicted y by passing x to the model
        y_pred = model(x)
        # Compute and print loss
        loss = criterion(y_pred, torch.max(y, 1)[1])
        if t % 10 == 9:
            os.system('cls')
            print('\nlearning rate = ', optimizer.state_dict()['param_groups'][0]['lr'])
            print('epoch=', t + 1, '\n针对训练集的损失', loss.item())
            _, predicted = torch.max(y_pred.data, 1)
            _, expected = torch.max(y.data, 1)
            correct = (predicted == expected).sum().item()
            print('针对训练集的准确率', (correct / (T_NUM*T_SIZE-VAL_SIZE)) * 100, '%')
            with torch.no_grad():
                test_y_pred = model(test_x.float())
                test_loss = criterion(test_y_pred, torch.max(test_y, 1)[1])
                print('针对测试集的损失', test_loss.item())
                _, predicted = torch.max(test_y_pred.data, 1)
                _, expected = torch.max(test_y.data, 1)
                correct = (predicted == expected).sum().item()
                print('针对测试集的准确率', (correct/VAL_SIZE)*100, '%')
                if correct/VAL_SIZE > 0.95:
                    torch.save(model.state_dict(), 'model.pkl')
                    print('准确率达到阈值， 模型已保存')
                    exit()

        # Zero gradients, perform a backward pass, and update the weights.
        loss.backward()
        optimizer.step()
        if dynamically_adjust:
            with torch.no_grad():
                test_y_pred = model(test_x.float())
                test_loss = criterion(test_y_pred, torch.max(test_y, 1)[1])
            scheduler.step(test_loss)