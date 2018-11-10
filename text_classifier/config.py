# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08

PROBLEM_TYPE = [
    "与人物相关的案件",
    "某年某法院审理的案件数量",
    "某地区判决的毒品数量",
    "某地区判决的毒品均价",
    "某地区未成年犯罪比例",
    "某地区团队犯案比例",
    "某地区平均量刑",
    "某案件作案总人数",
    "某案件的涉案人员最小年龄",
    "某案件的第一被告",
    "某案件第一被告判罚结果",
    "某案件的财产刑罚结果",
    "某案件出现的毒品信息",
    "某案件毒品单价"]
a = "all.seg300w50403.model"
b = "C:/Users/DrogoKhal/MachineLearning/Paper/baidu_encyclopedia/baidu_encyclopedia"

WORD_VECTOR_MODEL_PATH = a

TRAIN_CSV_PATH = "11-11_train_samples_15classes.csv"  # "11-11_train_samples_7classes"
TEST_CSV_PATH = "11-11_train_samples_15classes.csv"  # "test_samples_7_labels.csv"
JIEBA_USERDICT_PATH = "judicial_userdict_11_11.txt"

CLASSES_NUM = len(PROBLEM_TYPE)  # 11-11 classes num

MAX_SENTENCE_LENGTH = 15
WORD_EMBEDDING_DIM = 300
