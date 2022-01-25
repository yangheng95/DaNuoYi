# -*- coding: utf-8 -*-
# file: main.py.py
# time: 2021/7/29
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
from argparse import ArgumentParser

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from evolution.evolution import SingleTaskEvolution, MultiTaskEvolution
from utils.logger import Logger
from utils.net_utils import download_runtime_materials

download_runtime_materials()

def start_evolve(tasks: list, args, logger, rnd_select):
    if len(tasks) > 1:
        engine = MultiTaskEvolution(tasks, args.pop_size, logger)
    else:
        engine = SingleTaskEvolution(tasks, args.pop_size, logger)

    bypass_case_per_generation = {task: [] for task in tasks}

    for i in tqdm(range(args.evolve_round)):
        engine.evolve(gen_id=i, rnd_select=rnd_select)
        for task in tasks:
            bypass_case_per_generation[task].append([i, engine.count_by_task[task]])
        print('Found bypass cases:{}'.format(engine.count_by_task))

    logger.log_injections(engine.bypass_injection_by_task)

    for task in tasks:
        bypass_case_per_generation_by_task = np.array(bypass_case_per_generation[task])
        x = bypass_case_per_generation_by_task[:, 0]
        y = bypass_case_per_generation_by_task[:, 1]
        plt.plot(x, y, color='r', marker='o', linestyle='dashed')
        plt.xlabel('generation')
        plt.ylabel('bypass cases')
        if rnd_select:
            plt.title('(Rand) injection:{} classifier:{}\ntasks:{}'.format(task, args.classifier, tasks))
        else:
            plt.title('injection:{} classifier:{}\ntasks:{}'.format(task, args.classifier, tasks))
        plt.savefig(logger.output_figure_paths[logger.task_to_index[task]])
        plt.show()
        plt.close()


def quick_run(tasks=None, classifier_name='lstm', repeat=1, rnd_select=False):
    """

    :param tasks: Any subset from ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]
    :param classifier_name: Any from ['lstm', 'rnn', 'gru']
    :param repeat: Total experiment rounds
    :param rnd_select: Disable fitness-based individual selection
    :return:
    """
    if tasks is None:
        tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]

    arguments = ArgumentParser()
    arguments.add_argument("--tasks", default=tasks, type=list, help="injection tasks")
    arguments.add_argument("--classifier", default=classifier_name, choices=['lstm', 'rnn', 'gru'], help="Type of classifier to load")
    arguments.add_argument("--evolve_round", default=50, help="Maximum number of fuzzing rounds")
    arguments.add_argument("--pop_size", default=100, help="Fuzzing step size for each round (parallel fuzzing steps)")
    arguments.add_argument("--seed", default=list(range(repeat)), help="Fuzzing step size for each round (parallel fuzzing steps)")
    arguments = arguments.parse_args()

    logger = Logger(arguments.tasks, arguments.classifier)

    start_evolve(arguments.tasks, arguments, logger, rnd_select)


if __name__ == '__main__':

    rand_select = False  # 随机选择实现
    multi_processing = False  # 在CUDA内存足够的情况下并行运行单/多任务

    injection_tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]

    classifiers = ['lstm', 'rnn', 'gru']

    # quick_run(injection_tasks, 'lstm', rand_select)
    quick_run(injection_tasks, 'rnn', rand_select)
    # quick_run(injection_tasks, 'gru', rand_select)

    # injection_tasks = ["sqli"]
    # injection_tasks = ["xss"]
    # injection_tasks = ["osi"]
    # injection_tasks = ["phpi"]
    # injection_tasks = ["xmli"]
    # injection_tasks = ["htmli"]
    # for t in injection_tasks:
    #     for classifier in classifiers:
    #         if multi_processing:
    #
    #             multiprocessing.Process(target=quick_run, args=([t], classifier, rand_select)).start()
    #
    #         else:
    #             quick_run([t], classifier, rand_select)
    #
    # sys.exit(0)
