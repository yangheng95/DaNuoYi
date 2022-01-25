# -*- coding: utf-8 -*-
# file: bypass.py
# time: 2021/7/29
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import random

import requests

from DaNuoYi.evolution.entity.individual import Individual
from DaNuoYi.global_config import NGX_LUA_WAF, MODSECURITY_WAF, TIMEOUT


def construct_user_input(payload):
    payload = payload.replace(' ', '')
    payload = payload.replace('[blank]', ' ')
    payload = payload.replace('[terDigitExcludingZero]', str(random.randint(1, 10)))
    return payload


def is_bypass(individual: Individual, waf_address, return_code=False):

    try:
        session = requests.session()
        session.keep_alive = False

        task = individual.task
        individual = individual.injection

        payload = construct_user_input(individual)

        if '9999' in waf_address:
            if task == 'sqli':
                url_get = waf_address + r'sqli_6.php'
                params = {"title": payload, "action": "search"}
                response = session.get(url=url_get, params=params, timeout=TIMEOUT)
            elif task == 'xss':
                url_get = waf_address + r'xss_post.php'
                params = {"firstname": payload, "lastname": payload, "form": "submit"}
                response = session.get(url=url_get, params=params)
            elif task == 'phpi':
                url_get = waf_address + r'phpi.php?'
                params = {"message": payload}
                response = session.get(url=url_get, params=params)
            elif task == 'osi':
                url_get = waf_address + r'commandi.php?'
                params = {"target": payload, "form": "submit"}
                response = session.get(url=url_get, params=params)
            elif task == 'xmli':
                url_get = waf_address + r'xmli_2.php?'
                params = {"genre": payload, "action": "search"}
                response = session.get(url=url_get, params=params)
            elif task == 'htmli':
                url_get = waf_address + r'htmli_get.php?'
                params = {"firstname": payload, "lastname": payload, "form": "submit"}
                response = session.get(url=url_get, params=params)
            else:
                raise KeyError('Unknown injection type!')
        elif '8888' in waf_address:
            url_get = waf_address
            params = {"title": payload, "action": "search"}
            response = session.get(url=url_get, params=params, timeout=TIMEOUT)
        elif '7777' in waf_address:
            url_get = waf_address
            params = {"title": payload, "action": "search"}
            try:
                response = session.get(url=url_get, params=params, timeout=TIMEOUT)
            except Exception as e:
                print('Exception in bypass checking: {}'.format(e))
                return False, 800 if return_code else False
        else:
            raise KeyError('Unrecognized WAF address: {}!'.format(waf_address))

        if response.status_code == 200:
            return (True, response.status_code) if return_code else True

        return (False, response.status_code) if return_code else False

    except Exception as e:
        return is_bypass(individual, waf_address, return_code)
