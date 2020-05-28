import torch
import torch.nn as nn
import torch.nn.functional as functional


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
        self.soft = nn.Softmax(dim=1)
        self.dropout = torch.nn.Dropout(p=0.2)


    def forward(self, x):
        x = self.pool(functional.relu(self.conv1(x)))
        x = self.pool(functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * ((((self.HEIGH-4)//2)-4)//2) * ((((self.WIDTH-4)//2)-4)//2))
        x = self.dropout(functional.relu(self.fc1(x)))
        x = self.dropout(functional.relu(self.fc2(x)))
        x = self.fc3(x)
        x = self.soft(x)
        return x