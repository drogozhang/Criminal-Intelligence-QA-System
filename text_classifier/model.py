# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08


import torch.nn as nn
import torch.nn.functional as F


class BiLSTMTextClassifier(nn.Module):
    def __init__(self, word_embedding_dim, hidden_nodes, classes_num):
        super(BiLSTMTextClassifier, self).__init__()
        self.bilstm = nn.LSTM(word_embedding_dim, hidden_nodes, bidirectional=True)
        self.linear1 = nn.Linear(hidden_nodes * 2, hidden_nodes)
        self.linaer2 = nn.Linear(hidden_nodes, classes_num)

        self.cross_entropy_loss = nn.CrossEntropyLoss()

        self.optimizer = None

    def forward(self, x):
        result, hn = self.bilstm(x)
        result = result[-1]
        result = self.linear1(result)
        result = self.linaer2(result)
        return result

    def calc_loss(self, result, labels):
        return self.cross_entropy_loss(result, labels)

    def back_propogation(self, loss):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return


class CNNTextClassifier(nn.Module):
    def __init__(self, word_embedding_dim, classes_num, feature_maps, kernal_length, pooling_height, max_length):
        super(CNNTextClassifier, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1,
                      out_channels=feature_maps,
                      kernel_size=(kernal_length, word_embedding_dim),
                      stride=1,
                      padding=(1, 0)
                      ),
            nn.ReLU(),
        )
        self.pooling_height = pooling_height
        self.pooling_out = (max_length - kernal_length + 1) / pooling_height
        self.linear1 = nn.Linear(feature_maps * self.pooling_out, classes_num)

        self.cross_entropy_loss = nn.CrossEntropyLoss()

        self.optimizer = None

    def forward(self, x):
        result = F.max_pool2d(self.conv1(x), (self.pooling_height, 1))
        result = result.view(result.size()[0], -1)
        result = self.linear1(result)
        return result

    def calc_loss(self, result, labels):
        return self.cross_entropy_loss(result, labels)

    def back_propogation(self, loss):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return
