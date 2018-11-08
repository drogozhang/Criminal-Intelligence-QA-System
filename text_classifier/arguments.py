# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08

import os
import torch as t

from text_classifier import config as cfg

class TrainArguments(object):
    def __init__(self, classes_num=cfg.CLASSES_NUM, train_csv_path=cfg.TRAIN_CSV_PATH,
                 word_embedding_dim=cfg.WORD_EMBEDDING_DIM,
                 word_vector_model_path=cfg.WORD_VECTOR_MODEL_PATH,
                 hidden_nodes=100, learning_rate=1e-4, weight_decay=1e-3,
                 dropout_rate=0.5, max_epoch=100, accuracy_th=0.5,
                 prevent_overfitting_method="L2 Penalty"):
        # super(BaseAruguments, self).__init__()
        self.classes_num = classes_num
        self.train_csv_path = train_csv_path  # type str
        self.word_embedding_dim = word_embedding_dim
        self.word_vector_model_path = word_vector_model_path
        self.prevent_overfitting_method = prevent_overfitting_method  # due to small train samples, usually use L2 penalty to prevent over fitting
        self.hidden_nodes = hidden_nodes
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.dropout_rate = dropout_rate
        self.max_epoch = max_epoch
        self.accuracy_th = accuracy_th
        # self.jieba_userdict_path = cfg.JIEBA_USERDICT_PATH
        self.train_sentences = None
        self.train_labels = None

    def show_arguments(self):  # todo
        print("Train Samples from:" + " " * 6, self.train_csv_path, end="\n" * 2)
        print("Word Embedding dimension:" + " " * 6, self.word_embedding_dim, end="\n" * 2)
        print("Prevent Over Fitting Method:" + " " * 6, self.prevent_overfitting_method, end="\n" * 2)
        print("Word Vector Model:" + " " * 6, self.word_vector_model_path.split("\\")[-1], end="\n" * 2)
        if self.prevent_overfitting_method == "L2 Penalty":
            print("Penalty Weight Decay:" + " " * 6, self.weight_decay, end="\n" * 2)
        elif self.prevent_overfitting_method == "Dropout":
            print("Dropout Rate:" + " " * 6, self.dropout_rate, end="\n" * 2)
        print("Max Epoch:" + " " * 6, self.max_epoch, end="\n" * 2)
        print("Accuracy Threshold:" + " " * 6, self.accuracy_th, end="\n" * 2)
        return

    def get_save_folder(self, epoch):  # todo return one save path
        save_dictionary = "./" + str(self.classes_num) + "_classes" + \
                          self.word_vector_model_path.split("\\")[-1] + "/"
        if not os.path.exists(save_dictionary):
            os.makedirs(save_dictionary)
        return save_dictionary + "model_epoch" + str(epoch)

    def save_model(self, text_classsifier, epoch):
        save_path = self.get_save_folder(epoch)
        t.save(text_classsifier.state_dict(), save_path)
        print("Model Save in:", save_path)
        return

    def evaluation(self, ):  # todo
        return

    def save_criterion(self, ):  # todo
        return


class TestArguments(object):  # todo
    def __init__(self, classes_num=cfg.CLASSES_NUM, train_csv_path=cfg.TRAIN_CSV_PATH,
                 word_embedding_dim=cfg.WORD_EMBEDDING_DIM,
                 word_vector_model_path=cfg.WORD_VECTOR_MODEL_PATH, ):  # todo to be filled about test arguments
        # super(TestArguments).__init__(classes_num)
        self.train_csv_path = train_csv_path  # type str
        self.word_embedding_dim = word_embedding_dim
        self.word_vefctor_model_path = word_vector_model_path
