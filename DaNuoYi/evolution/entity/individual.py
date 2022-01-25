# -*- coding: utf-8 -*-
# file: individual.py
# time: 2021/7/30
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

from DaNuoYi.evolution.fuzzer import Fuzzer
from DaNuoYi.injection_utils.payload import Payload


class Individual:
    def __init__(self, task):
        self.injection = Payload(task).injection
        self.task = task
        self.fitness = 0

    def mutate(self):
        fuzzer = Fuzzer(self.injection)
        injection = fuzzer.fuzz()
        inj = Individual(self.task)
        inj.injection = injection
        return inj

    def __lt__(self, other):
        return self.fitness < other.fitness
