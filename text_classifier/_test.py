# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-09

import torch as t
from torch.autograd import Variable
import jieba
import numpy as np
from text_classifier.arguments import TestArguments
from text_classifier.model import BiLSTMTextClassifier
import text_classifier.config as cfg
from text_classifier.utils import sentence2matrix, load_word_vector_model

jieba_userdict_path = cfg.JIEBA_USERDICT_PATH
jieba.load_userdict(jieba_userdict_path)
stacked = True
base_model = "LSTM"
advanced_model = "LSTM"
base_model_epoch = 146  # need change
advanced_model_epoch = 146
test_arguments = TestArguments(stacked, base_model_epoch, advanced_model_epoch, base_model=base_model,
                               advanced_model=advanced_model)
test_arguments.show_arguments()
# key word list
key_word_ls = open(jieba_userdict_path, "r", encoding="utf-8").readlines()
key_word_ls = [item.strip("\n") for item in key_word_ls]
key_word_ls.append("xx")
# load base model
base_text_classifier = BiLSTMTextClassifier(test_arguments.word_embedding_dim, test_arguments.hidden_nodes,
                                            test_arguments.base_classes_num).cuda()
base_model_load_path = test_arguments.get_load_folder(base_model_epoch, base=True)
base_text_classifier.load_state_dict(t.load(base_model_load_path))
print("Load Base Model from ", base_model_load_path)

# load advanced model
advanced_text_classifier = BiLSTMTextClassifier(test_arguments.word_embedding_dim, test_arguments.hidden_nodes,
                                                test_arguments.advanced_classes_num).cuda()
advanced_model_load_path = test_arguments.get_load_folder(advanced_model_epoch, base=False)
advanced_text_classifier.load_state_dict(t.load(advanced_model_load_path))
print("Load Advanced Model from ", advanced_model_load_path)

# word_vector_model
word_vector_model = load_word_vector_model(test_arguments.word_vector_model_path)
empty_wv = np.zeros((1, test_arguments.word_embedding_dim))


def predict(original_sentence):  # todo overwrite
    """Input:
            original_sentence: str
        Return:
            advanced_problem: boolean
            predict_result: int
            catched_key_words: list of str which is key words of criminal system
        Description: Input the original sentence from the front
        if advanced problem :
            return True, predicted problem type, key words
        else:
            return False, predicted problem type, key words"""
    word_segmentation_ls = list(jieba.cut(original_sentence))
    if len(word_segmentation_ls) == 1 and word_segmentation_ls[0] in key_word_ls:
        return False, 1, word_segmentation_ls
    sentence_matrix, catched_key_words = sentence2matrix(word_segmentation_ls, word_vector_model, empty_wv, key_word_ls,
                                                         test_arguments, test_arguments.base_model)
    sentence_matrix = Variable(t.Tensor(sentence_matrix)).cuda()
    base_predict_score = base_text_classifier.forward(sentence_matrix).data.cpu().numpy()
    base_predict_result = np.argmax(base_predict_score)
    if base_predict_result == 1:
        return False, base_predict_result, catched_key_words
    else:
        print(test_arguments.base_problem_type[base_predict_result])
        advanced_predict_score = advanced_text_classifier.forward(sentence_matrix).data.cpu().numpy()
        advanced_predict_result = np.argmax(advanced_predict_score)
        if "甲基苯丙胺" in catched_key_words:
            catched_key_words[catched_key_words.index("甲基苯丙胺")] = "冰毒"
        return True, advanced_predict_result, catched_key_words


def main():
    all_sentences = open("final_test.txt", "r").readlines()
    all_sentences = [item.strip("\n") for item in all_sentences]
    for original_sentence in all_sentences:
        print("Original Sentence:  ", original_sentence)
        advanced_problem, predict_result, catched_key_words = predict(original_sentence)
        if advanced_problem:
            print("Problem type:  ", test_arguments.advanced_problem_type[predict_result])
        else:
            print("Problem type:  ", test_arguments.base_problem_type[predict_result])

        print("Catched Key Words:  ", catched_key_words, end="\n" * 2)


if __name__ == '__main__':
    main()
