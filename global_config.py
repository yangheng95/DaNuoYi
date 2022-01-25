# -*- coding: utf-8 -*-
# file: global_config.py
# time: 2021/7/29
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os.path

#############################  General Config  #############################
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = 'output'  # path to save result
RETRY_TIME = 60

#############################  Network Config  #############################
MODSECURITY_SERVER_IP = r'http://159.75.238.202:9999/'  # Web app address
OPENRESTY_SERVER_IP = r'http://159.75.238.202:9999/'  # Web app address
TIMEOUT = 1000  # default patience in network connection

###########################  Classifier Config  ############################
CASE_NUM_PER_TASK = 1000  # number of injections used for training surrogate classifier
REMOVE_SAME_INJECTION = True  # number of injections used for training surrogate classifier

##############################  Google Drive  ##############################
