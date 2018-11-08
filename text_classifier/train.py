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
from text_classifier.model import BiLSTMTextClassifier

import text_classifier.config as cfg
from text_classifier.utils import sentence2matrix, load_word_vector_model

jieba_userdict_path = cfg.JIEBA_USERDICT_PATH
jieba.load_userdict(jieba_userdict_path)


def train_epoch(train_arguments, text_classifier):
    losses = []
    correct = 0
    for train_sample_index in range(len(train_arguments.train_sentences)):
        input_x = Variable(t.Tensor(train_arguments.train_sentences[train_sample_index])).cuda()
        result = text_classifier.forward(input_x)
        gt_cls = Variable(t.Tensor([train_arguments.train_labels[train_sample_index]]).long()).cuda()
        loss = text_classifier.calc_loss(result, gt_cls)
        losses.append(loss.data.cpu().numpy())

        pred_cls = np.argmax(F.softmax(result).data.cpu().numpy())
        if pred_cls == gt_cls:
            correct += 1
        # bptt
        text_classifier.back_propogation(loss)
    return np.mean(np.array(losses)), correct / len(train_arguments.train_sentences)


def start_training(train_arguments):
    text_classifier = BiLSTMTextClassifier(train_arguments.word_embedding_dim, train_arguments.hidden_nodes,
                                           train_arguments.classes_num).cuda()
    if train_arguments.prevent_overfitting_method == "L2 Penalty":
        text_classifier.optimizer = optim.Adam(text_classifier.parameters(), lr=train_arguments.learning_rate,
                                               weight_decay=train_arguments.weight_decay)
    if train_arguments.prevent_overfitting_method == "None":
        text_classifier.optimizer = optim.Adam(text_classifier.parameters(), lr=train_arguments.learning_rate)
    accuracy_th = 0.5  # at least accuracy > 0.5, we save the text_classifier
    for epoch_index in range(train_arguments.max_epoch):
        epoch_loss, accuracy = train_epoch(train_arguments, text_classifier)
        print("Epoch:   ", epoch_index+1, "Epoch Loss:   ", epoch_loss, "Accuracy:   {}%".format(accuracy * 100))
        if accuracy > accuracy_th or accuracy == 1:
            accuracy_th = accuracy
            train_arguments.save_model(text_classifier, epoch_index + 1)


def prepare_train_date(train_arguments):
    empty_wv = np.zeros((1, train_arguments.word_embedding_dim))

    key_word_ls = open(jieba_userdict_path, "r", encoding="utf-8").readlines()
    key_word_ls.append("xx")
    word_vector_model = load_word_vector_model(train_arguments.word_vector_model_path)

    # create train samples
    train_samples = open(train_arguments.train_csv_path, "r").readlines()

    train_original_sentence = [item.split(",")[0] for item in train_samples]
    train_arguments.train_labels = [int(item.split(",")[1].strip("\n")) - 1 for item in train_samples]  # start from 0

    cut_sentence_ls = []
    train_sentences = []
    for original_sentence in train_original_sentence:
        cut_sentence_ls.append([item for item in jieba.cut(original_sentence)])
        train_sentences.append(
            sentence2matrix([item for item in jieba.cut(original_sentence)], word_vector_model, empty_wv, key_word_ls))

    train_arguments.train_sentences = train_sentences
    return


def main():
    max_epoch = 1000
    prevent_overfitting_method = "None"
    train_arguments = TrainArguments(max_epoch=max_epoch, prevent_overfitting_method=prevent_overfitting_method)
    train_arguments.show_arguments()
    prepare_train_date(train_arguments)
    start_training(train_arguments)


if __name__ == '__main__':
    main()
