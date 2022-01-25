# -*- coding: utf-8 -*-
# file: injection_generation.py
# time: 2021/8/1
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os

from tqdm import tqdm

from DaNuoYi import global_config
from DaNuoYi.evolution.entity.individual import Individual
from DaNuoYi.utils.bypass import is_bypass


def generate_injection_cases(task, save_cases=True):
    if save_cases:
        injection_cases_path = '{}/runtime_materials/injection_cases/{}/'.format(global_config.PROJECT_PATH, task)
        if not os.path.exists(injection_cases_path):
            os.makedirs(injection_cases_path)
        fout_pass = open('{}/{}_pass.txt'.format(injection_cases_path, task), mode='w', encoding='utf8')
        fout_block = open('{}/{}_block.txt'.format(injection_cases_path, task), mode='w', encoding='utf8')
        fout_sum = open('{}/{}.txt'.format(injection_cases_path, task), mode='w', encoding='utf8')

    pool = set()

    pass_injections = []
    block_injections = []
    for _ in tqdm(range(global_config.CASE_NUM_PER_TASK), postfix='generating injection_utils cases for {} ...'.format(task)):
        inj = Individual(task)

        if global_config.REMOVE_SAME_INJECTION:
            while inj.injection.strip() in pool:
                inj = Individual(task)
                pool.add(inj.injection.strip())

        if is_bypass(task, inj)[0]:
            pass_injections.append(inj.injection.strip() + '$BYPASS_LABEL$1')
            if save_cases:
                fout_pass.write(inj.injection.strip() + '$BYPASS_LABEL$1\n')
                fout_sum.write(inj.injection.strip() + '$BYPASS_LABEL$1\n')
        else:
            block_injections.append(inj.injection.strip() + '$BYPASS_LABEL$0')
            if save_cases:
                fout_block.write(inj.injection.strip() + '$BYPASS_LABEL$0\n')
                fout_sum.write(inj.injection.strip() + '$BYPASS_LABEL$0\n')

    print('Bypass cases:{}'.format(len(pass_injections)))
    print('Block cases:{}'.format(len(block_injections)))
    return pass_injections + block_injections, pass_injections, block_injections
