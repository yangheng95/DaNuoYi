# -*- coding: utf-8 -*-
# file: generate_translated_case.py
# time: 2021/8/7
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
from DaNuoYi.deep_learning.translator.translator import InjectionTranslator

injection_tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]

cases = 30000

if __name__ == '__main__':
    for task1 in injection_tasks:
        for task2 in injection_tasks:
            if task1 != task2:
                translator = InjectionTranslator(task1, task2)
