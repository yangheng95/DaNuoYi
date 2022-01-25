# -*- coding: utf-8 -*-
# file: fitness_assigner.py
# time: 2021/7/31
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import pickle

import torch
from autocuda import auto_cuda
from findfile import find_file, find_dir

from DaNuoYi import global_config
from DaNuoYi.deep_learning.classifier.classifier_model import RNNClassifier
from DaNuoYi.deep_learning.classifier.dataset_utils import build_tokenizer, build_embedding_matrix
from DaNuoYi.evolution.entity.individual import Individual


class FitnessAssigner:
    def __init__(self, task, classifier):
        self.injection_type = task

        state_dict_dir = find_dir(global_config.PROJECT_PATH, ['classification_datasets', task])

        state_dict_path = find_file(state_dict_dir, [classifier, 'state_dict'])  # model of best performance
        opt_path = find_file(state_dict_dir, [classifier, 'opt'])  # model of best performance
        embedding_path = find_file(state_dict_dir, 'embedding_matrix')

        self.opt = pickle.load(open(opt_path, 'rb'))
        self.opt.device = torch.device(auto_cuda())

        dataset_files = {
            'train': find_file(global_config.PROJECT_PATH, task + '_train.txt', recursive=True),
            'test': find_file(global_config.PROJECT_PATH, task + '_test.txt', recursive=True),
        }

        self.tokenizer = build_tokenizer(
            fnames=[dataset_files['train'], dataset_files['test']],
            max_seq_len=self.opt.max_seq_len)
        self.embedding_matrix = build_embedding_matrix(
            word2idx=self.tokenizer.word2idx,
            embed_dim=self.opt.embed_dim,
            dat_fname=embedding_path)

        self.classifier = RNNClassifier(self.embedding_matrix, self.opt).to(self.opt.device)

        self.classifier.load_state_dict(torch.load(state_dict_path, map_location=self.opt.device))

        self.classifier.eval()
        torch.autograd.set_grad_enabled(False)


    def assign_fitness(self, injection):
        # assert isinstance(injection_utils, Individual) or isinstance(injection_utils, Population)

        if isinstance(injection, Individual):
            injection = [injection]

        injection_ids = []
        for inj in injection:
            injection_ids.append(self.tokenizer.text_to_sequence(inj.injection))

        injection_ids = torch.tensor(injection_ids).to(self.opt.device)

        fitness = self.classifier([injection_ids])
        for i, fit in enumerate(fitness):
            injection[i].fitness = fit.item()
