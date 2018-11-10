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

test_model_epoch = 161  # need change
test_arguments = TestArguments(test_model_epoch)
test_arguments.show_arguments()
# key word list
key_word_ls = open(jieba_userdict_path, "r", encoding="utf-8").readlines()
key_word_ls = [item.strip("\n") for item in key_word_ls]
key_word_ls.append("xx")
# model
text_classifier = BiLSTMTextClassifier(test_arguments.word_embedding_dim, test_arguments.hidden_nodes,
                                       test_arguments.classes_num).cuda()
text_classifier.load_state_dict(t.load(test_arguments.get_load_folder(test_arguments.model_epoch)))
print("Load model from ", test_arguments.get_load_folder(test_model_epoch))
# word_vector_model
word_vector_model = load_word_vector_model(test_arguments.word_vector_model_path)
empty_wv = np.zeros((1, test_arguments.word_embedding_dim))


def predict(original_sentence):
    """Input:
            original_sentence: str
        Return:
            predict_result: int
            catched_key_words: list of str which is key words of criminal system
        Description: Input the original sentence from the front
        and return the key words and predict the problem type"""
    word_segmentation_ls = list(jieba.cut(original_sentence))
    sentence_matrix, catched_key_words = sentence2matrix(word_segmentation_ls, word_vector_model, empty_wv, key_word_ls,
                                                         test_arguments)
    sentence_matrix = Variable(t.Tensor(sentence_matrix)).cuda()
    predict_score = text_classifier.forward(sentence_matrix).data.cpu().numpy()
    predict_result = np.argmax(predict_score)
    return predict_result, catched_key_words


def main():
    all_sentences = open("final_test.txt", "r").readlines()
    all_sentences = [item.split(",")[0] for item in all_sentences ]
    for original_sentence in all_sentences:
        print("Original Sentence:  ", original_sentence)
        predict_result, catched_key_words = predict(original_sentence)
        print("Problem type:  ", test_arguments.problem_type[predict_result])
        print("Catched Key Words:  ", catched_key_words, end="\n" * 2)


if __name__ == '__main__':
    main()
