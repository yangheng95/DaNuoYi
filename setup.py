# -*- coding: utf-8 -*-
# file: setup.py.py
# time: 2021/8/12
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
from pathlib import Path

from setuptools import setup, find_packages
cwd = Path(__file__).parent
long_description = (cwd / "README.MD").read_text(encoding='utf8')
setup(
    name='DaNuoYi',
    version='0.2.0',
    description='This package provide the interface to run multitask evolutionary injection generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yangheng95/DaNuoYi',
    # Author details
    author='Heng, Yang',
    author_email='yangheng@exeter.ac.uk',
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    exclude_package_date={'': ['.gitignore']},
    # Choose your license
    license='MIT',
    install_requires=['opennmt-py==2.1.2', 'torchtext', 'findfile', 'autocuda', 'googledrivedownloader', 'torch', 'termcolor', 'tqdm', 'matplotlib'],
)
