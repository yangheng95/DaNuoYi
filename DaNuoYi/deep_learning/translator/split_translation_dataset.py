# -*- coding: utf-8 -*-
# file: split_translation_dataset.py
# time: 2021/8/6
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os.path

from findfile import find_file

from DaNuoYi import global_config


def split_translation_datasets():
    injection_tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]

    # for task1 in injection_tasks:
    #     for task2 in injection_tasks:
    #         if task1 != task2:
    #             __split_translation_dataset__(task1, task2)

    __split_translation_dataset__('xmli', 'osi')


def __split_translation_dataset__(task1, task2):
    source_raw_data_path = find_file(global_config.PROJECT_PATH, '{}2{}_source.txt'.format(task1, task2))
    target_raw_data_path = find_file(global_config.PROJECT_PATH, '{}2{}_target.txt'.format(task1, task2))
    source_raw_data = open(source_raw_data_path, mode='r').readlines()
    target_raw_data = open(target_raw_data_path, mode='r').readlines()

    train_source_path = source_raw_data_path.replace(os.path.basename(source_raw_data_path), 'src-train.txt')
    train_target_path = target_raw_data_path.replace(os.path.basename(target_raw_data_path), 'tgt-train.txt')

    test_source_path = source_raw_data_path.replace(os.path.basename(source_raw_data_path), 'src-val.txt')
    test_target_path = target_raw_data_path.replace(os.path.basename(target_raw_data_path), 'tgt-val.txt')

    f_train_source = open(train_source_path, mode='w', encoding='utf8')
    f_train_target = open(train_target_path, mode='w', encoding='utf8')

    f_test_source = open(test_source_path, mode='w', encoding='utf8')
    f_test_target = open(test_target_path, mode='w', encoding='utf8')

    for i, (s, t) in enumerate(zip(source_raw_data, target_raw_data)):
        if i + 1 < len(source_raw_data) * 0.8:
            f_train_source.write(s)
            f_train_target.write(t)
        else:
            f_test_source.write(s)
            f_test_target.write(t)


if __name__ == '__main__':
    split_translation_datasets()
