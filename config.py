# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08

import os

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
father_path += "/"

ADVANCED_PROBLEM_TYPE = [
    "与人物相关的案件",
    "某年某法院审理的案件数量",
    "某地区判决的毒品数量",
    "某地区判决的毒品均价",
    "某地区青年人犯罪比例",
    "某地区团队犯案比例",
    "某地区平均量刑"]

BASE_PROBLEM_TYPE = ["高级问题，我要好好推理，请稍等",
                     "智障问题，不会自己看结点吗？"]
a = "text_classifier/insurance_wv_model"
b = "C:/Users/DrogoKhal/MachineLearning/Paper/baidu_encyclopedia/baidu_encyclopedia"

WORD_VECTOR_MODEL_PATH = a

TRAIN_BASE_CSV_PATH = "text_classifier/11-12_base_advanced_problems_train_samples_14classes.csv"
TRAIN_ADVANCED_CSV_PATH = "text_classifier/11-12_advanced_problem_train_samples_7classes.csv"

TEST_ADVANCED_CSV_PATH = "text_classifier/11-12_advanced_problem_train_samples_7classes.csv"  # "test_samples_7_labels.csv"

JIEBA_USERDICT_PATH = "judicial_userdict_11_12.txt"
BASE_CLASSES_NUM = 2
ADVANCED_CLASSES_NUM = len(ADVANCED_PROBLEM_TYPE)  # 11-11 classes num

MAX_SENTENCE_LENGTH = 15  # for CNN text classifier
WORD_EMBEDDING_DIM = 300
