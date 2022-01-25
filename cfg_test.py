# -*- coding: utf-8 -*-
# file: cfg_test.py
# time: 2021/9/24
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import tqdm

from DaNuoYi.utils.bypass import is_bypass
from DaNuoYi.global_config import LUA_RESTY_WAF, MODSECURITY_WAF, NGX_LUA_WAF
from DaNuoYi.evolution.entity.individual import Individual
CASE_NUMBER = 100000

for t in ["htmli"]:
    Unique = set()
    UniqueLuaPass = set()
    UniqueModPass = set()
    UniqueNgxPass = set()
    for _ in tqdm.tqdm(range(CASE_NUMBER), postfix=t):
        individual = Individual(t)
        if individual.injection not in Unique:
            Unique.add(individual.injection)
            if is_bypass(individual, LUA_RESTY_WAF):
                UniqueLuaPass.add(individual.injection)

            if is_bypass(individual, MODSECURITY_WAF):
                UniqueModPass.add(individual.injection)

            if is_bypass(individual, NGX_LUA_WAF):
                UniqueNgxPass.add(individual.injection)

    print('------------------- {} -------------------'.format(t.upper()))
    print('Total Case Number: {}'.format(CASE_NUMBER))
    print('Unique Case Number: {}'.format(len(Unique)))
    print('Unique Pass Case Number (LUA_RESTY_WAF): {}'.format(len(UniqueLuaPass)))
    print('Unique Pass Case Number (MODSECURITY_WAF): {}'.format(len(UniqueModPass)))
    print('Unique Pass Case Number (NGX_LUA_WAF): {}'.format(len(UniqueNgxPass)))
    print('-----------------------------------------------')
