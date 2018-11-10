# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08

import os
import torch as t

from text_classifier import config as cfg


# class BaseAruguments:
#     def __int__(self, classes_num):
#         self.classes_num = classes_num
#
# word_embedding_dim, classes_num, feature_maps, kernal_length, pooling_height, max_length


class TrainArguments:
    def __init__(self, model="LSTM", classes_num=cfg.CLASSES_NUM, train_csv_path=cfg.TRAIN_CSV_PATH,
                 word_embedding_dim=cfg.WORD_EMBEDDING_DIM,
                 problem_type=cfg.PROBLEM_TYPE, test_csv_path=cfg.TEST_CSV_PATH,
                 word_vector_model_path=cfg.WORD_VECTOR_MODEL_PATH,
                 hidden_nodes=100, learning_rate=1e-4, weight_decay=1e-3,
                 dropout_rate=0.5, max_epoch=100, accuracy_th=0.5, feature_maps=36,
                 kernal_length=4, max_length=15, pooling_height=4,
                 prevent_overfitting_method="L2 Penalty"):
        self.model = model
        self.classes_num = classes_num
        self.train_csv_path = train_csv_path  # type str
        self.test_csv_path = test_csv_path
        self.problem_type = problem_type
        self.feature_maps = feature_maps
        self.kernal_length = kernal_length
        self.max_length = max_length
        self.pooling_height = pooling_height

        self.word_embedding_dim = word_embedding_dim
        self.word_vector_model_path = word_vector_model_path
        self.prevent_overfitting_method = prevent_overfitting_method
        self.hidden_nodes = hidden_nodes
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.dropout_rate = dropout_rate
        self.max_epoch = max_epoch
        self.accuracy_th = accuracy_th
        self.train_sentences = None
        self.test_sentences = None
        self.train_labels = None
        self.test_labels = None

    def show_arguments(self):  # todo
        print("Model:" + " " * 6, self.model, end="\n" * 2)
        print("Train Samples from:" + " " * 6, self.train_csv_path, end="\n" * 2)
        print("Test Samples from:" + " " * 6, self.test_csv_path, end="\n" * 2)
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
        save_dictionary = "./" + self.model + "_" + str(self.classes_num) + "_classes_" + \
                          self.word_vector_model_path.split("/")[-1] + "/"
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


class TestArguments:
    def __init__(self, model_epoch, classes_num=cfg.CLASSES_NUM,
                 word_embedding_dim=cfg.WORD_EMBEDDING_DIM,
                 problem_type=cfg.PROBLEM_TYPE,
                 weight_decay=1e-3, prevent_overfitting_method="L2 Penalty",
                 word_vector_model_path=cfg.WORD_VECTOR_MODEL_PATH,
                 dropout_rate=0.5, hidden_nodes=100, model="LSTM",
                 ):  # todo to be filled about test arguments
        self.model_epoch = model_epoch
        self.classes_num = classes_num
        self.word_embedding_dim = word_embedding_dim
        self.word_vector_model_path = word_vector_model_path
        self.prevent_overfitting_method = prevent_overfitting_method
        self.weight_decay = weight_decay
        self.dropout_rate = dropout_rate
        self.hidden_nodes = hidden_nodes
        self.problem_type = problem_type
        self.model = model

    def show_arguments(self):
        print("Model :" + " " * 6, self.model, end="\n" * 2)
        print("Model Epoch :" + " " * 6, self.model_epoch, end="\n" * 2)
        print("Word Embedding dimension:" + " " * 6, self.word_embedding_dim, end="\n" * 2)
        print("Prevent Over Fitting Method:" + " " * 6, self.prevent_overfitting_method, end="\n" * 2)
        print("Word Vector Model:" + " " * 6, self.word_vector_model_path.split("\\")[-1], end="\n" * 2)
        if self.prevent_overfitting_method == "L2 Penalty":
            print("Penalty Weight Decay:" + " " * 6, self.weight_decay, end="\n" * 2)
        elif self.prevent_overfitting_method == "Dropout":
            print("Dropout Rate:" + " " * 6, self.dropout_rate, end="\n" * 2)
        return

    def get_load_folder(self, epoch):
        load_dictionary = "./" + self.model + "_" + str(self.classes_num) + "_classes_" + \
                          self.word_vector_model_path.split("/")[-1] + "/"
        return load_dictionary + "model_epoch" + str(epoch)
