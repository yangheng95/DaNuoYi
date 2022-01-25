# -*- coding: utf-8 -*-
# file: train_classifier.py
# time: 2021/7/31
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import argparse
import math
import os
import pickle
import random

import numpy
import torch
import torch.nn as nn
import tqdm
from autocuda import auto_cuda
from findfile import find_file
from sklearn import metrics
from torch.utils.data import DataLoader

from DaNuoYi import global_config
from DaNuoYi.deep_learning.classifier.classifier_model import RNNClassifier
from DaNuoYi.deep_learning.classifier.dataset_utils import build_tokenizer, build_embedding_matrix, ClassifierDataset


class Instructor:
    def __init__(self, opt):
        self.opt = opt
        state_dict = os.path.join(os.path.join(self.opt.dirname, 'classification_datasets'), self.opt.dataset)
        if not os.path.exists(state_dict):
            os.makedirs(state_dict)
        tokenizer = build_tokenizer(
            fnames=[opt.dataset_file['train'], opt.dataset_file['test']],
            max_seq_len=opt.max_seq_len)
        embedding_matrix = build_embedding_matrix(
            word2idx=tokenizer.word2idx,
            embed_dim=opt.embed_dim,
            dat_fname='{}/{}_{}_embedding_matrix.dat'.format(state_dict, str(opt.embed_dim), opt.dataset))

        self.trainset = ClassifierDataset(opt.dataset_file['train'], tokenizer)
        self.testset = ClassifierDataset(opt.dataset_file['test'], tokenizer)

        self.model = RNNClassifier(embedding_matrix, opt).to(opt.device)

        # self._print_args()

    def _print_args(self):
        n_trainable_params, n_nontrainable_params = 0, 0
        for p in self.model.parameters():
            n_params = torch.prod(torch.tensor(p.shape))
            if p.requires_grad:
                n_trainable_params += n_params
            else:
                n_nontrainable_params += n_params
        print('> n_trainable_params: {0}, n_nontrainable_params: {1}'.format(n_trainable_params, n_nontrainable_params))
        print('> training arguments:')
        for arg in vars(self.opt):
            print('>>> {0}: {1}'.format(arg, getattr(self.opt, arg)))

    def _reset_params(self):
        for child in self.model.children():
            for p in child.parameters():
                if p.requires_grad:
                    if len(p.shape) > 1:
                        self.opt.initializer(p)
                    else:
                        stdv = 1. / math.sqrt(p.shape[0])
                        torch.nn.init.uniform_(p, a=-stdv, b=stdv)

    def _train(self, criterion, optimizer, train_data_loader, test_data_loader):
        max_test_epoch = 0
        max_test_f1 = 0
        max_test_acc = 0
        global_step = 0
        model_save_path = None
        for i_epoch in tqdm.tqdm(range(self.opt.num_epoch)):
            print('epoch: {}'.format(i_epoch))
            n_correct, n_total, loss_total = 0, 0, 0
            # switch model to training mode
            for i_batch, batch in enumerate(train_data_loader):
                self.model.train()
                global_step += 1
                # clear gradient accumulators
                optimizer.zero_grad()

                inputs = [batch[col].to(self.opt.device) for col in self.opt.inputs_cols]
                outputs = self.model(inputs)
                targets = batch['bypass'].to(self.opt.device)
                outputs = outputs.view(outputs.shape[0])
                loss = criterion(outputs, targets.float())
                loss.backward()
                optimizer.step()

                n_correct += ((outputs > 0.5).int() == targets).sum().item()
                n_total += len(outputs)
                loss_total += loss.item() * len(outputs)
                if global_step % self.opt.log_step == 0:
                    train_acc = n_correct / n_total
                    train_loss = loss_total / n_total
                    print('loss: {:.4f}, acc: {:.4f}'.format(train_loss, train_acc))

                    test_acc, test_f1 = self._evaluate_acc_f1(test_data_loader)
                    print('> test_acc: {:.4f}, test_f1: {:.4f}'.format(test_acc, test_f1))
                    if test_acc > max_test_acc:
                        max_test_acc = test_acc
                        max_test_epoch = i_epoch
                        if not os.path.exists('{0}/{1}/'.format(
                                os.path.join(self.opt.dirname, 'classification_datasets'),
                                self.opt.dataset,
                        )):
                            os.mkdir('{0}/{1}/'.format(
                                os.path.join(self.opt.dirname, 'classification_datasets'),
                                self.opt.dataset,
                            ))
                        if model_save_path:
                            os.remove(model_save_path)
                        model_save_path = '{0}/{1}/{2}_{3}_test_acc_{4}_test_f1_{5}.state_dict'.format(
                            os.path.join(self.opt.dirname, 'classification_datasets'),
                            self.opt.dataset,
                            self.opt.dataset,
                            self.opt.classifier_name,
                            round(test_acc, 4),
                            round(test_f1, 4),
                        )

                        self.model.cpu()
                        torch.save(self.model.state_dict(), model_save_path)
                        self.model.to(self.opt.device)
                        opt_save_path = '{0}/{1}/{2}_{3}.opt'.format(
                            os.path.join(self.opt.dirname, 'classification_datasets'),
                            self.opt.dataset,
                            self.opt.dataset,
                            self.opt.classifier_name,
                        )
                        pickle.dump(self.opt, open(opt_save_path, 'wb'))
                        print('>> saved: {}'.format(model_save_path))
                    if test_f1 > max_test_f1:
                        max_test_f1 = test_f1
                    if i_epoch - max_test_epoch >= self.opt.patience:
                        print('>> early stop.')
                        break

        return model_save_path

    def _evaluate_acc_f1(self, data_loader):
        n_correct, n_total = 0, 0
        t_targets_all, t_outputs_all = None, None
        # switch model to evaluation mode
        self.model.eval()
        with torch.no_grad():
            for i_batch, t_batch in enumerate(data_loader):
                t_inputs = [t_batch[col].to(self.opt.device) for col in self.opt.inputs_cols]
                t_targets = t_batch['bypass'].to(self.opt.device)
                t_outputs = self.model(t_inputs)

                t_outputs = t_outputs.view(t_outputs.shape[0])
                n_correct += ((t_outputs > 0.5).int() == t_targets).sum().item()
                n_total += len(t_outputs)

                if t_targets_all is None:
                    t_targets_all = t_targets
                    t_outputs_all = t_outputs
                else:
                    t_targets_all = torch.cat((t_targets_all, t_targets), dim=0)
                    t_outputs_all = torch.cat((t_outputs_all, t_outputs), dim=0)

        acc = n_correct / n_total
        f1 = metrics.f1_score(t_targets_all.cpu(), (t_outputs_all > 0.5).cpu(), labels=[0, 1], average='macro')
        return acc, f1

    def run(self):
        # Loss and Optimizer
        # criterion = nn.CrossEntropyLoss()
        criterion = nn.BCELoss()
        _params = filter(lambda p: p.requires_grad, self.model.parameters())
        optimizer = self.opt.optimizer(_params, lr=self.opt.lr, weight_decay=self.opt.l2reg)

        train_data_loader = DataLoader(dataset=self.trainset, batch_size=self.opt.batch_size, shuffle=True)
        test_data_loader = DataLoader(dataset=self.testset, batch_size=self.opt.batch_size, shuffle=False)

        self._train(criterion, optimizer, train_data_loader, test_data_loader)


def train(task='htmli', classifier='lstm'):
    # Hyper Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--classifier_name', default=classifier, choices=['lstm', 'rnn', 'gru'], type=str)
    parser.add_argument('--dataset', default=task, choices=["sqli", "xss", "osi", "phpi", "xmli", "htmli"], type=str)
    parser.add_argument('--optimizer', default='adam', type=str)
    parser.add_argument('--initializer', default='xavier_uniform_', type=str)
    parser.add_argument('--lr', default=1e-3, type=float, help='learning rate')
    parser.add_argument('--dropout', default=0.5, type=float)
    parser.add_argument('--l2reg', default=0.001, type=float)
    parser.add_argument('--num_epoch', default=5, type=int, help='try larger number for non-BERT models')
    parser.add_argument('--batch_size', default=64, type=int, help='try 16, 32, 64 for BERT models')
    parser.add_argument('--log_step', default=10, type=int)
    parser.add_argument('--embed_dim', default=128, type=int)
    parser.add_argument('--max_seq_len', default=60, type=int)
    parser.add_argument('--out_dim', default=1, type=int)
    parser.add_argument('--patience', default=5, type=int)
    parser.add_argument('--device', default=auto_cuda(), type=str, help='e.g. cuda:0')
    parser.add_argument('--seed', default=666, type=int, help='set seed for reproducibility')
    opt = parser.parse_args()

    if opt.seed is not None:
        random.seed(opt.seed)
        numpy.random.seed(opt.seed)
        torch.manual_seed(opt.seed)
        torch.cuda.manual_seed(opt.seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        os.environ['PYTHONHASHSEED'] = str(opt.seed)

    dirname, filename = os.path.split(os.path.abspath(__file__))
    opt.dirname = dirname

    dataset_files = {
        'train': find_file(global_config.PROJECT_PATH, task + '_train.txt', recursive=True),
        'test': find_file(global_config.PROJECT_PATH, task + '_test.txt', recursive=True),
    }

    input_colses = ['injection_ids', 'bypass']

    initializers = {
        'xavier_uniform_': torch.nn.init.xavier_uniform_,
        'xavier_normal_': torch.nn.init.xavier_normal_,
        'orthogonal_': torch.nn.init.orthogonal_,
    }
    optimizers = {
        'adadelta': torch.optim.Adadelta,  # default lr=1.0
        'adagrad': torch.optim.Adagrad,  # default lr=0.01
        'adam': torch.optim.Adam,  # default lr=0.001
        'adamax': torch.optim.Adamax,  # default lr=0.002
        'asgd': torch.optim.ASGD,  # default lr=0.01
        'rmsprop': torch.optim.RMSprop,  # default lr=0.01
        'sgd': torch.optim.SGD,
    }

    opt.dataset_file = dataset_files
    opt.inputs_cols = input_colses
    opt.initializer = initializers[opt.initializer]
    opt.optimizer = optimizers[opt.optimizer]
    opt.device = torch.device(opt.device)

    ins = Instructor(opt)
    ins.run()


def train_classifier_by_task(task):
    print('Classifier training begin for {}'.format(task))
    train(task, 'lstm')
    train(task, 'rnn')
    train(task, 'gru')
    print('Classifier training done for {}'.format(task))


if __name__ == '__main__':
    # tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]
    # tasks = ["sqli"]
    # tasks = ["sqli", "xss"]
    # tasks = ["osi", "phpi"]
    tasks = ["xmli", "htmli"]
    for t in tasks:
        train_classifier_by_task(t)
