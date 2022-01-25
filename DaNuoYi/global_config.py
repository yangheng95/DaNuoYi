# -*- coding: utf-8 -*-
# file: global_config.py
# time: 2021/7/29
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os.path

#############################  General Config  #############################
PROJECT_PATH = os.getcwd()
# PROJECT_PATH = 'E:/works/injection'
OUTPUT_PATH = 'output'  # path to save result
REGENERATE_COUNT = 100
RETRY_TIME = 60

###############################  WAF Config  ###############################
MODSECURITY_WAF = r'http://159.75.238.202:9999/'  # Web app address
NGX_LUA_WAF = r'http://159.75.238.202:8888/'  # Web app address
LUA_RESTY_WAF = r'http://159.75.238.202:7777/'  # Web app address
OPEN_WAF = r'http://159.75.238.202:6666/'  # Web app address

###########################  Classifier Config  ############################
CASE_NUM_PER_TASK = 1000  # number of injections used for training surrogate classifier
REMOVE_SAME_INJECTION = True  # number of injections used for training surrogate classifier

###############################  NET Config  ###############################
TIMEOUT = 1000  # default patience in network connection
