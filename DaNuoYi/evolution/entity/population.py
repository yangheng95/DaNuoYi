# -*- coding: utf-8 -*-
# file: entity.py
# time: 2021/7/30
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

from DaNuoYi.evolution.entity.individual import Individual


class Population:
    def __init__(self, injection_type, pop_size=100):
        self.injection_type = injection_type
        self.individuals = [Individual(injection_type) for _ in range(pop_size)]

    def get_average_fitness(self):
        return sum([idv.fitness for idv in self.individuals]) / len(self.individuals)

    def __iter__(self):
        for idv in self.individuals:
            yield idv

    def __getitem__(self, item):
        return self.individuals[item]

    def __len__(self):
        return len(self.individuals)
