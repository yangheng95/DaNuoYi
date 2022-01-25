# -*- coding: utf-8 -*-
# file: word2vec.py
# time: 2021/7/30
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import os
import time

from findfile import find_files
from gensim.models import Word2Vec

# from gensim.models.word2vec import LineSentence
import DaNuoYi.global_config


def train_word2vec(workers=1):
    '''
    LineSentence(inp)：格式简单：一句话=一行; 单词已经过预处理并被空格分隔。
    size：是每个词的向量维度；
    window：是词向量训练时的上下文扫描窗口大小，窗口为5就是考虑前5个词和后5个词；
    min-count：设置最低频率，默认是5，如果一个词语在文档中出现的次数小于5，那么就会丢弃；
    workers：是训练的进程数（需要更精准的解释，请指正），默认是当前运行机器的处理器核数。这些参数先记住就可以了。
    sg ({0, 1}, optional) – 模型的训练算法: 1: skip-gram; 0: CBOW
    alpha (float, optional) – 初始学习率
    iter (int, optional) – 迭代次数，默认为5
    '''
    in_corpus_path = find_files('injection_cases', key='.txt', recursive=True)
    while len(in_corpus_path) < 18:
        time.sleep(global_config.RETRY_TIME)
        in_corpus_path = find_files('injection_cases', key='.txt', recursive=True)

    in_corpus = []
    for p in in_corpus_path:
        fin = open(p, mode='r', encoding='utf8')
        in_corpus.extend([line.split('$BYPASS_LABEL$')[0].strip() for line in fin.readlines()])
        fin.close()

    print('Training word2vec ...')

    save_path = os.path.join(global_config.PROJECT_PATH, 'runtime_materials/word2vec')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    model = Word2Vec(in_corpus, vector_size=128, window=5, min_count=5, sg=1, workers=workers, epochs=50)
    model.wv.save_word2vec_format(os.path.join(save_path, 'w2v.txt'), binary=False)  # 不以C语言可以解析的形式存储词向量
    model.save(os.path.join(save_path, 'w2v.model'))
    print('Word2vec training done ...')
