# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-08

import numpy as np

import gensim
from gensim.models import Word2Vec


def sentence2matrix(str_ls, word_vector_model, empty_wv, key_word_ls):
    sentence_matrix = []
    for word in str_ls:
        if word in key_word_ls:  # if the word is key word, then we do not use word vector! use empty instead
            sentence_matrix.append(empty_wv)
        else:
            try:
                sentence_matrix.append(word_vector_model[word].reshape(1, word_vector_model[word].size))
            except KeyError:
                sentence_matrix.append(empty_wv)
    return np.array(sentence_matrix)


def list2str(ls):
    return "".join(ls)


def load_word_vector_model(word_vector_model_path):
    try:
        model = Word2Vec.load(word_vector_model_path)
    except Exception:
        model = gensim.models.KeyedVectors.load_word2vec_format(word_vector_model_path)

    return model
