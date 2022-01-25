# -*- coding: utf-8 -*-
# file: logger.py
# time: 2021/6/2 0002

# Copyright from https://www.cnblogs.com/c-x-a/p/9072234.html

import logging
import os
import time

from DaNuoYi.global_config import OUTPUT_PATH

today = time.strftime('%Y%m%d %H%M%S', time.localtime(time.time()))


class Logger:
    def __init__(self, tasks: list, classifier=''):
        self.tasks = tasks
        self.task_to_index = {task: i for i, task in enumerate(tasks)}
        self.classifier = classifier
        dir_name = OUTPUT_PATH

        self.output_injection_paths = []
        self.output_count_paths = []
        self.output_figure_paths = []

        if len(self.tasks) == 1:
            log_path = os.path.join(dir_name, "singletask/{}/".format(today))
            if not os.path.exists(log_path):
                os.makedirs(log_path)

        elif len(self.tasks) == 2:
            log_path = os.path.join(dir_name, "doubletask/{}/".format(today))
            if not os.path.exists(log_path):
                os.makedirs(log_path)

        else:
            log_path = os.path.join(dir_name, "multitask/{}/".format(today))
            if not os.path.exists(log_path):
                os.makedirs(log_path)

        self.output_injection_paths = [log_path + task + '_' + classifier + "_injections.txt" for task in self.tasks]
        self.output_count_paths = [log_path + task + "_" + classifier + "_count.txt" for task in self.tasks]
        self.output_figure_paths = [log_path + task + "_" + classifier + "_fig.png" for task in self.tasks]

        self.injection_loggers = self.init_loggers('injection')
        self.count_loggers = self.init_loggers('count')

    def init_loggers(self, log_type):

        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

        if log_type == 'count':
            full_paths = [os.path.join(output_count_path) for output_count_path in self.output_count_paths]
            loggers = [logging.getLogger('{}_{}_count'.format(task, self.classifier)) for task in self.tasks]
        else:
            full_paths = [os.path.join(output_injection_path) for output_injection_path in self.output_injection_paths]
            loggers = [logging.getLogger('{}_{}_injection'.format(task, self.classifier)) for task in self.tasks]

        for logger, full_path in zip(loggers, full_paths):
            if not logger.handlers:
                # 指定logger输出格式
                # formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

                # 文件日志
                file_handler = logging.FileHandler(full_path, mode='w', encoding="utf8")
                # file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
                file_handler.setLevel(logging.INFO)
                logger.addHandler(file_handler)

                # # 控制台日志
                # console_handler = logging.StreamHandler(sys.stdout)
                # console_handler.formatter = formatter  # 也可以直接给formatter赋值
                # console_handler.setLevel(logging.INFO)
                # logger.addHandler(console_handler)

                # 指定日志的最低输出级别，默认为WARN级别
                logger.setLevel(logging.INFO)

        return loggers

    def log_injections(self, injection_map):
        for task in self.tasks:
            for inj in injection_map[task]:
                self.injection_loggers[self.task_to_index[task]].info(inj)

    def log_count(self, count_map, gen_id):
        for task in self.tasks:
            self.count_loggers[self.task_to_index[task]].info('{}: {}'.format(gen_id, count_map[task]))
