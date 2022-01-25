# -*- coding: utf-8 -*-
# file: main.py.py
# time: 2021/7/29
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import random
from argparse import ArgumentParser

import numpy
import numpy as np
import torch
from matplotlib import pyplot as plt
from tqdm import tqdm

from DaNuoYi.evolution.evolution import SingleTaskEvolution, MultiTaskEvolution
from DaNuoYi.utils.logger import Logger
from DaNuoYi.utils.net_utils import download_runtime_materials


def start_evolve(tasks: list, args, logger, rnd_select):
    if len(tasks) > 1:
        engine = MultiTaskEvolution(args, logger)
    else:
        engine = SingleTaskEvolution(args, logger)

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
        plt.xlabel('Generation')
        plt.ylabel('Bypass Cases')
        if rnd_select:
            plt.title('(Rand) injection:{} Classifier:{} WAF:{} \nTasks:{}'.format(task, args.classifier, args.waf, tasks))
        else:
            plt.title('Injection:{} Classifier:{} WAF:{} \nTasks:{}'.format(task, args.classifier, args.waf, tasks))
        plt.savefig(logger.output_figure_paths[logger.task_to_index[task]])
        plt.show()
        plt.close()


def quick_run(tasks=None, classifier_name='lstm', waf='mod_security', seed=None, rnd_select=False):
    """

    :param tasks: Any subset from ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]
    :param waf: Choose from ['mod_security', 'ngx_lua_waf', 'lua_resty_waf']
    :param classifier_name: Any from ['lstm', 'rnn', 'gru']
    :param seed: random seed
    :param rnd_select: Disable fitness-based individual selection
    :return:
    """
    if tasks is None:
        tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]

    arguments = ArgumentParser()
    arguments.add_argument("--tasks", default=tasks, type=list, help="injection tasks")
    arguments.add_argument("--waf", default=waf, choices=['mod_security', 'openresty'])
    arguments.add_argument("--classifier", default=classifier_name, choices=['lstm', 'rnn', 'gru'], help="Type of classifier to load")
    arguments.add_argument("--evolve_round", default=50, help="Maximum number of fuzzing rounds")
    arguments.add_argument("--pop_size", default=100, help="Fuzzing step size for each round (parallel fuzzing steps)")
    arguments = arguments.parse_args()

    logger = Logger(arguments.tasks, arguments.classifier)
    download_runtime_materials()

    if seed:
        for sd in seed:
            random.seed(sd)
            numpy.random.seed(sd)
            torch.manual_seed(sd)
            torch.cuda.manual_seed(sd)
            start_evolve(arguments.tasks, arguments, logger, rnd_select)

    else:
        print('seed=None, start experiment mode (10 runs with random seeds for each trivial.)')
        for _ in range(10):
            start_evolve(arguments.tasks, arguments, logger, rnd_select)

if __name__ == "__main__":
    quick_run(waf='lua_resty_waf')
    quick_run(waf='ngx_lua_waf')
    quick_run(waf='mod_security')
