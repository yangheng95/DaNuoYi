# -*- coding: utf-8 -*-
# file: classifier_model.py
# time: 2021/7/30
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import torch
import torch.nn as nn

from DaNuoYi.deep_learning.classifier.dynamic_rnn import DynamicLSTM


class RNNClassifier(nn.Module):
    def __init__(self, embedding_matrix, opt):
        super(RNNClassifier, self).__init__()
        self.opt = opt
        self.embed = nn.Embedding.from_pretrained(torch.tensor(embedding_matrix, dtype=torch.float))
        self.lstm = DynamicLSTM(opt.embed_dim, opt.embed_dim, num_layers=1, batch_first=True, rnn_type=opt.classifier_name.upper())
        self.dense = nn.Linear(opt.embed_dim, opt.out_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, inputs):
        text_raw_indices = inputs[0]
        x = self.embed(text_raw_indices)
        x_len = torch.sum(text_raw_indices != 0, dim=-1)
        _, (h_n, _) = self.lstm(x, x_len)
        out = self.dense(h_n[0])
        return self.sigmoid(out)


class CNN(nn.Module):
    def __init__(self, embedding_matrix, opt):
        super(CNN, self).__init__()
        self.embed = nn.Embedding.from_pretrained(torch.tensor(embedding_matrix, dtype=torch.float))
        self.cnn = nn.Conv1d(in_channels=1, out_channels=1, kernel_size=(5, 3))
        self.dense = nn.Linear(opt.embed_dim, opt.num_label)

    def forward(self):
        pass
