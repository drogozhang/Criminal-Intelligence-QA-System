# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08

import os
import torch as t

from text_classifier import config as cfg


class TrainArguments:
    def __init__(self, stacked, base_model="LSTM", advanced_model="LSTM",
                 base_classes_num=cfg.BASE_CLASSES_NUM,
                 advanced_classes_num=cfg.ADVANCED_CLASSES_NUM,
                 train_base_csv_path=cfg.TRAIN_BASE_CSV_PATH,
                 train_advanced_csv_path=cfg.TRAIN_ADVANCED_CSV_PATH,
                 word_embedding_dim=cfg.WORD_EMBEDDING_DIM,
                 base_problem_type=cfg.BASE_PROBLEM_TYPE,
                 advanced_problem_type=cfg.ADVANCED_PROBLEM_TYPE,
                 test_advanced_csv_path=cfg.TEST_ADVANCED_CSV_PATH,
                 word_vector_model_path=cfg.WORD_VECTOR_MODEL_PATH,
                 hidden_nodes=100, learning_rate=1e-4, weight_decay=1e-3,
                 dropout_rate=0.5, max_epoch=100, accuracy_th=0.5, feature_maps=36,
                 kernal_length=4, max_length=15, pooling_height=4,
                 prevent_overfitting_method="L2 Penalty"):

        self.stacked = stacked
        self.base_model = base_model
        self.advanced_model = advanced_model
        self.base_classes_num = base_classes_num
        self.advanced_classes_num = advanced_classes_num
        self.train_base_csv_path = train_base_csv_path  # type str
        self.train_advanced_csv_path = train_advanced_csv_path
        self.test_advanced_csv_path = test_advanced_csv_path
        self.base_problem_type = base_problem_type
        self.advanced_problem_type = advanced_problem_type
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

        # for base model
        self.base_train_sentences = None
        self.base_train_labels = None
        # for advanced model
        self.advanced_train_sentences = None
        self.advanced_train_labels = None

    def show_arguments(self):
        print("Stacked:" + " " * 6, self.stacked, end="\n" * 2)
        print("Base Model:" + " " * 6, self.base_model, end="\n" * 2)
        print("Advanced Model:" + " " * 6, self.advanced_model, end="\n" * 2)
        print("Train Base Samples from:" + " " * 6, self.train_base_csv_path, end="\n" * 2)
        print("Train Advanced Samples from:" + " " * 6, self.train_advanced_csv_path, end="\n" * 2)
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

    def get_save_folder(self, epoch, base):
        save_dictionary = "./stacked_" if self.stacked else "./"
        save_dictionary += "base_cls_" + str(self.base_classes_num) + \
                           "_advanced_cls_" + str(self.advanced_classes_num) + "_classes_" + \
                           self.word_vector_model_path.split("/")[-1] + "/"
        save_dictionary += "base_model_" if base else "advanced_model_"
        save_dictionary += self.base_model + "/" if base else self.advanced_model + "/"
        if not os.path.exists(save_dictionary):
            os.makedirs(save_dictionary)
        return save_dictionary + "model_epoch" + str(epoch)

    def save_model(self, text_classsifier, epoch, base):
        save_path = self.get_save_folder(epoch, base)
        t.save(text_classsifier.state_dict(), save_path)
        print("Model Save in:", save_path)
        return

    def evaluation(self, ):  # todo
        return

    def save_criterion(self, ):  # todo
        return


class TestArguments:
    def __init__(self, stacked, base_model_epoch, advanced_model_epoch,
                 base_classes_num=cfg.BASE_CLASSES_NUM,
                 advanced_classes_num=cfg.ADVANCED_CLASSES_NUM,
                 word_embedding_dim=cfg.WORD_EMBEDDING_DIM,
                 base_problem_type=cfg.BASE_PROBLEM_TYPE,
                 advanced_problem_type=cfg.ADVANCED_PROBLEM_TYPE,
                 weight_decay=1e-3, prevent_overfitting_method="L2 Penalty",
                 word_vector_model_path=cfg.WORD_VECTOR_MODEL_PATH,
                 hidden_nodes=100,
                 base_model="LSTM", advanced_model="LSTM",
                 ):  # todo to be filled about test arguments

        self.stacked = stacked
        self.base_model_epoch = base_model_epoch
        self.advanced_model_epoch = advanced_model_epoch
        self.base_classes_num = base_classes_num
        self.advanced_classes_num = advanced_classes_num
        self.word_embedding_dim = word_embedding_dim
        self.word_vector_model_path = word_vector_model_path
        self.prevent_overfitting_method = prevent_overfitting_method
        self.weight_decay = weight_decay
        self.base_problem_type = base_problem_type
        self.advanced_problem_type = advanced_problem_type
        self.base_model = base_model
        self.advanced_model = advanced_model
        self.hidden_nodes = hidden_nodes

    def show_arguments(self):
        print("Stacked:" + " " * 6, self.stacked, end="\n" * 2)
        print("Base Model:" + " " * 6, self.base_model, end="\n" * 2)
        print("Advanced Model:" + " " * 6, self.advanced_model, end="\n" * 2)
        print("Base Model Epoch :" + " " * 6, self.base_model_epoch, end="\n" * 2)
        print("Advanced Model Epoch :" + " " * 6, self.base_model_epoch, end="\n" * 2)
        print("Word Embedding dimension:" + " " * 6, self.word_embedding_dim, end="\n" * 2)
        print("Word Vector Model:" + " " * 6, self.word_vector_model_path.split("\\")[-1], end="\n" * 2)
        return

    def get_load_folder(self, epoch, base):
        load_dictionary = "./stacked_" if self.stacked else "./"
        load_dictionary += "base_cls_" + str(self.base_classes_num) + \
                           "_advanced_cls_" + str(self.advanced_classes_num) + "_classes_" + \
                           self.word_vector_model_path.split("/")[-1] + "/"
        load_dictionary += "base_model_" if base else "advanced_model_"
        load_dictionary += self.base_model + "/" if base else self.advanced_model + "/"
        return load_dictionary + "model_epoch" + str(epoch)
