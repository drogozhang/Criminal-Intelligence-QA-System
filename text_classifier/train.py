# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08


import jieba
import numpy as np
import torch as t
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from text_classifier.arguments import TrainArguments
from text_classifier.model import BiLSTMTextClassifier, CNNTextClassifier

import text_classifier.config as cfg
from text_classifier.utils import sentence2matrix, load_word_vector_model

jieba_userdict_path = cfg.JIEBA_USERDICT_PATH
jieba.load_userdict(jieba_userdict_path)
empty_wv = np.zeros((1, cfg.WORD_EMBEDDING_DIM))


def train_epoch(sentences, labels, text_classifier, model="LSTM", train_flag=True):
    losses = []
    correct = 0
    for train_sample_index in range(len(sentences)):
        if model == "LSTM":
            input_x = Variable(t.Tensor(sentences[train_sample_index])).cuda()
        else:
            shape = sentences[train_sample_index].shape
            input_x = Variable(t.Tensor(sentences[train_sample_index].reshape(1, 1, shape[0], shape[2]))).cuda()
        result = text_classifier.forward(input_x)
        gt_cls = Variable(t.Tensor([labels[train_sample_index]]).long()).cuda()
        loss = text_classifier.calc_loss(result, gt_cls)
        losses.append(loss.data.cpu().numpy())

        pred_cls = np.argmax(F.softmax(result).data.cpu().numpy())
        if pred_cls == gt_cls:
            correct += 1
        # bptt
        if train_flag:
            text_classifier.back_propogation(loss)
    return np.mean(np.array(losses)), correct / len(sentences)


def start_training(train_arguments, base):
    print('===========================================')
    if base:
        if train_arguments.base_model == "LSTM":
            text_classifier = BiLSTMTextClassifier(train_arguments.word_embedding_dim, train_arguments.hidden_nodes,
                                                   train_arguments.base_classes_num).cuda()
        else:
            text_classifier = CNNTextClassifier(train_arguments.word_embedding_dim, train_arguments.base_classes_num,
                                                train_arguments.feature_maps, train_arguments.kernal_length,
                                                train_arguments.pooling_height, train_arguments.max_length).cuda()
        print("Start Training Base Model: ", train_arguments.base_model)
    else:
        if train_arguments.advanced_model == "LSTM":
            text_classifier = BiLSTMTextClassifier(train_arguments.word_embedding_dim, train_arguments.hidden_nodes,
                                                   train_arguments.advanced_classes_num).cuda()

        else:
            text_classifier = CNNTextClassifier(train_arguments.word_embedding_dim,
                                                train_arguments.advanced_classes_num,
                                                train_arguments.feature_maps, train_arguments.kernal_length,
                                                train_arguments.pooling_height, train_arguments.max_length).cuda()
        print("Start Training Advanced Model: ", train_arguments.advanced_model)
    print('===========================================')
    if train_arguments.prevent_overfitting_method == "L2 Penalty":
        text_classifier.optimizer = optim.Adam(text_classifier.parameters(), lr=train_arguments.learning_rate,
                                               weight_decay=train_arguments.weight_decay)
    if train_arguments.prevent_overfitting_method == "None":
        text_classifier.optimizer = optim.Adam(text_classifier.parameters(), lr=train_arguments.learning_rate)
    min_loss = 1e5
    for epoch_index in range(train_arguments.max_epoch):
        if base:
            train_sentences, train_labels = train_arguments.base_train_sentences, train_arguments.base_train_labels
        else:
            train_sentences, train_labels = train_arguments.advanced_train_sentences, train_arguments.advanced_train_labels
        model = train_arguments.base_model if base else train_arguments.advanced_model
        epoch_loss, accuracy = train_epoch(train_sentences, train_labels,
                                           text_classifier, model)
        if epoch_index % 5 == 0:
            print("Epoch:   ", epoch_index + 1, "Epoch Loss:   ", epoch_loss, "Accuracy:   {}%".format(accuracy * 100))
            if accuracy >= train_arguments.accuracy_th and epoch_loss < min_loss:
                min_loss = epoch_loss
                train_arguments.accuracy_th = accuracy
                train_arguments.save_model(text_classifier, epoch_index + 1, base)


def prepare_date(samples_path, word_vector_model, train_arguments, model):
    key_word_ls = open(jieba_userdict_path, "r", encoding="utf-8").readlines()
    key_word_ls = [item.strip("\n") for item in key_word_ls]
    key_word_ls.append("xx")

    # create train samples
    samples = open(samples_path, "r").readlines()
    original_sentences = [item.split(",")[0] for item in samples]

    labels = [int(item.split(",")[1].strip("\n")) for item in samples]  # start from 0

    cut_sentence_ls = []
    matrix_sentence_ls = []
    for original_sentence in original_sentences:
        word_segmentation_ls = list(jieba.cut(original_sentence))
        cut_sentence_ls.append(word_segmentation_ls)
        sentence_matrix, _ = sentence2matrix(word_segmentation_ls, word_vector_model, empty_wv, key_word_ls,
                                             train_arguments, model)
        matrix_sentence_ls.append(sentence_matrix)

    return matrix_sentence_ls, labels


def main():
    max_epoch = 150
    prevent_overfitting_method = "L2 Penalty"
    base_model = "LSTM"  # "CNN"
    advanced_model = "LSTM"
    stacked = True
    train_arguments = TrainArguments(stacked, base_model=base_model, advanced_model=advanced_model,
                                     max_epoch=max_epoch,
                                     prevent_overfitting_method=prevent_overfitting_method)
    train_arguments.show_arguments()
    word_vector_model = load_word_vector_model(train_arguments.word_vector_model_path)

    train_arguments.base_train_sentences, train_arguments.base_train_labels = prepare_date(
        train_arguments.train_base_csv_path,
        word_vector_model, train_arguments, base_model)

    train_arguments.advanced_train_sentences, train_arguments.advanced_train_labels = prepare_date(
        train_arguments.train_advanced_csv_path,
        word_vector_model, train_arguments, advanced_model)

    start_training(train_arguments, True)   # train base
    start_training(train_arguments, False)  # train advance


if __name__ == '__main__':
    main()
