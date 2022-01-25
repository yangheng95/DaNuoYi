# DaNuoYi - Evolutionary Multitask Injection Generation Tool
[![PyPI](https://img.shields.io/pypi/v/DaNuoYi)](https://pypi.org/project/DaNuoYi/)
![License](https://img.shields.io/pypi/l/DaNuoYi?logo=DaNuoYi)

## Context-free Grammar for Injection Generation
DaNuoYi uses the context-free grammar to generates the injection cases, and it is available at [here](DaNuoYi/injection_utils/payload).

There is also a [document](document/context-free-grammar.pdf) which briefly describes the context-free grammar injection generation.

## Usage

### Install DaNuoYi from pip or Source Code
For the purpose of easy to use, we build the DaNuoYi package from the source codes, and it is available at PyPi package library now. 
It is recommended to create a new environment and install DaNuoYi PyPi,
```bash
pip install DaNuoYi
```
or install from the source code,

```bash
git clone https://github.com/COLA-Laboratory/DaNuoYi
cd DaNuoYi
pip install .
```

### Running
Now we can run injection generation as following:
```python3
"""
    quick_run accepts the following params:

    :param tasks: Any subset from ["sqli", "xss", "osi", "phpi", "xmli", "htmli"], tasks=None means running multitask injection generation
    :param waf: Choose from ['mod_security', 'ngx_lua_waf', 'lua_resty_waf'], three WAFs are supported currently.
    :param classifier_name: Any from ['lstm', 'rnn', 'gru']
    :param seed: random seed, the number of randoms is also the round of the experiments
    :param rnd_select: Disable fitness-based individual selection
    :return:
"""

import random
import time

import torch

from DaNuoYi import quick_run

seeds = [random.randint(1, 1000000) for _ in range(21)]

torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='lstm', waf='mod_security', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='rnn', waf='mod_security', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='gru', waf='mod_security', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='lstm', waf='lua_resty_waf', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='rnn', waf='lua_resty_waf', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='gru', waf='lua_resty_waf', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='lstm', waf='ngx_lua_waf', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='rnn', waf='ngx_lua_waf', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)
quick_run(classifier_name='gru', waf='ngx_lua_waf', seed=seeds, rnd_select=False)
torch.cuda.empty_cache()
time.sleep(5)

```
### Experiment Results Visualization
- The distribution of the bypassing test injections count on Ngx-Lua-WAF over 10 runs under the same search budget.

[![NGX-Lua-WAF](document/box_ngx.pdf)
- The distribution of the bypassing test injections count on Lua-Resty over 10 runs under the same search budget.

[![LUA-Resty-WAF](document/box_lua.pdf)
- The distribution of the bypassing test injections count on ModSecurity over 10 runs under the same search budget.
- 
[![ModSecurity-WAF](document/box_mod.pdf)



