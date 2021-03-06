import torch
import numpy as np
import os
import torch.optim.lr_scheduler as lr_scheduler
from parameter import *
from model import Net, device


def get_dir_num(path):
    return len([lists for lists in os.listdir(path) if os.path.isdir(os.path.join(path, lists))])

def get_file_num(path):
    return len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))])


if __name__ == '__main__':
    print(device)

    path1 = './data/MAC1/'
    c_num = get_dir_num(path1)
    for c in range(7, c_num+1):
        total = 0
        path2 = path1 + 'State' + str(c) + '/'
        t_num = get_dir_num(path2)
        for t in range(1, t_num + 1):
            path3 = path2 + 'T' + str(t) + '/'
            p_num = min(get_file_num(path3), 200)
            for p in range(1, p_num + 1):
                total += 1
                # print(total)
        if c in [1, 2, 4]:
            NPY_SIZE = 50
        elif c in [3, 5, 6]:
            NPY_SIZE = 100
        else:
            NPY_SIZE = 150
        x = torch.zeros((total, NPY_SIZE, NFFT), device=device)
        y = torch.zeros((total, OUTPUT_SIZE), device=device)
        cnt = 0
        path2 = path1 + 'State' + str(c) + '/'
        t_num = get_dir_num(path2)
        for t in range(1, t_num+1):
            path3 = path2 + 'T' + str(t) + '/'
            p_num = min(get_file_num(path3), 200)
            for p in range(1, p_num + 1):
                path4 = path3 + 'T' + str(t) + '_' + str(p) + '.npy'
                # raw data
                temp_x = np.load(path4)
                temp_y = t - 1
                # process x from complete number to real number
                for k in range(NPY_SIZE):
                    temp_x[k] = abs(temp_x[k])
                temp_x = torch.from_numpy(temp_x.astype('float64'))[0:NPY_SIZE]
                # clean and normalize data
                for k in [0, 29, 30, 31, 32, 33, 34, 35]:
                    temp_x[:, k] = 0
                for k in range(temp_x.shape[0]):
                    CSI_max = temp_x[k].max()
                    for p in range(temp_x.shape[1]):
                        temp_x[k][p] = temp_x[k][p] / CSI_max
                x[cnt] = temp_x
                y[cnt][temp_y] = 1
                print(c, temp_y, y[cnt])
                cnt += 1


        # Extract test batch
        x = torch.reshape(x, (total, 1, NPY_SIZE, NFFT))
        # test_x = torch.zeros((VAL_SIZE, NPY_SIZE, NFFT), device=device)
        # test_y = torch.zeros((VAL_SIZE, OUTPUT_SIZE), device=device)
        # for i in range(VAL_SIZE):
        #     n = random.randint(0, x.shape[0] - 1)
        #     # print(n)
        #     test_x[i] = x[n]
        #     test_y[i] = y[n]
        # test_x = torch.reshape(test_x, (VAL_SIZE, 1, NPY_SIZE, NFFT))
        x.requires_grad = True
        y.requires_grad = True
        # Construct our model by instantiating the class defined above
        model = Net(NPY_SIZE, NFFT, OUTPUT_SIZE).to(device)

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
            print(y_pred)
            # Compute and print loss
            loss = criterion(y_pred, torch.max(y, 1)[1])
            if t % 10 == 9:
                os.system('cls')
                print('\nlearning rate = ', optimizer.state_dict()['param_groups'][0]['lr'])
                print('epoch=', t + 1, '\n针对训练集的损失', loss.item())
                _, predicted = torch.max(y_pred.data, 1)
                _, expected = torch.max(y.data, 1)
                correct = (predicted == expected).sum().item()
                print('针对训练集的准确率', (correct / (total-VAL_SIZE)) * 100, '%')
                with torch.no_grad():
                    # test_y_pred = model(test_x.float())
                    # test_loss = criterion(test_y_pred, torch.max(test_y, 1)[1])
                    # print('针对测试集的损失', test_loss.item())
                    # _, predicted = torch.max(test_y_pred.data, 1)
                    # _, expected = torch.max(test_y.data, 1)
                    # correct = (predicted == expected).sum().item()
                    # print('针对测试集的准确率', (correct/VAL_SIZE)*100, '%')
                    if correct/total > 0.95:
                        torch.save(model.state_dict(), 'models/model' + str(c) + '.pkl')
                        print('准确率达到阈值， 模型已保存')
                        break

            # Zero gradients, perform a backward pass, and update the weights.
            loss.backward()
            optimizer.step()
            # if dynamically_adjust:
            #     with torch.no_grad():
            #         test_y_pred = model(test_x.float())
            #         test_loss = criterion(test_y_pred, torch.max(test_y, 1)[1])
            #     scheduler.step(test_loss)
