# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08


import torch.nn as nn


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
