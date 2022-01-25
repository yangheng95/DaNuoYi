# -*- coding: utf-8 -*-
# file: prepare_runtime_materials.py
# time: 2021/8/2
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import multiprocessing
import os
import random
import shutil
import time

import tqdm
from findfile import find_file
from gensim import corpora, models, similarities
from termcolor import colored

from DaNuoYi import global_config
from DaNuoYi.deep_learning.classifier.train_classifier import train_classifier_by_task
from DaNuoYi.evolution.entity.individual import Individual
from DaNuoYi.global_config import LUA_RESTY_WAF, MODSECURITY_WAF, NGX_LUA_WAF
from DaNuoYi.injection_utils.injection_generation import generate_injection_cases
from DaNuoYi.utils.bypass import is_bypass
from DaNuoYi.deep_learning.word2vec.word2vec import train_word2vec


def injection_bypass_check(injection_tasks, multi_process=False):
    for t in injection_tasks:
        if multi_process:
            multiprocessing.Process(target=__injection_bypass_check__, args=(t,)).start()
        else:
            __injection_bypass_check__(t)


def __injection_bypass_check__(task):
    # filter_f_path = find_file(global_config.PROJECT_PATH, '{}.filter.txt'.format(task))
    filter_f_path = find_file(global_config.PROJECT_PATH, '{}_filter_pass.txt'.format(task))
    # filter_f_path = find_file(global_config.PROJECT_PATH, '{}_filter_block.txt'.format(task))
    fin = open(filter_f_path, mode='r', encoding='utf8')
    injections = []
    pass_injections = []
    block_injections = []

    for line in fin.readlines():
        if line.strip() not in injections:
            injections.append(line.strip())
    print('loaded {} injections: {}'.format(task, len(injections)))

    status_code_set = set()
    count = 0
    temp_idv = Individual(task)
    for i, inj in enumerate(injections):
        temp_idv.injection = inj
        # pass_res, status_code = is_bypass(temp_idv, MODSECURITY_WAF, return_code=True)
        # pass_res, status_code = is_bypass(temp_idv, NGX_LUA_WAF, return_code=True)
        pass_res, status_code = is_bypass(temp_idv, LUA_RESTY_WAF, return_code=True)
        if pass_res:
            count += 1
            print(colored('{}:  {} --> {}'.format(i, status_code, inj), 'green'))
            pass_injections.append(inj)
        else:
            print(colored('{}:  {} --> {}'.format(i, status_code, inj), 'red'))
            block_injections.append(inj)

        status_code_set.add(status_code)
    print('Bypass cases: {}'.format(count))
    print('Status code set: {}'.format(status_code_set))

    fout_pass = open(
        find_file(global_config.PROJECT_PATH, '{}_pass.txt'.format(task)).replace('_pass.txt', '_filter_pass.txt'),
        mode='a+',
        encoding='utf8'
    )

    for inj in pass_injections:
        fout_pass.write(inj + '\n')
    print('{} finished!'.format(find_file(global_config.PROJECT_PATH, '{}_filter_pass.txt'.format(task))))

    fout_block = open(
        find_file(global_config.PROJECT_PATH, '{}_block.txt'.format(task)).replace('_block.txt', '_filter_block.txt'),
        mode='a+',
        encoding='utf8'
    )
    for inj in block_injections:
        fout_block.write(inj + '\n')
    print('{} finished!'.format(find_file(global_config.PROJECT_PATH, '{}_filter_block.txt'.format(task))))


def generate_classification_dataset(task, sum_injections=None):
    base_dir = os.path.join(os.path.dirname(__file__), 'classifier')
    if not sum_injections:
        pass_data_dir = find_file(global_config.PROJECT_PATH, '{}_filter_pass.txt'.format(task), exclude_key='v1', recursive=True)
        block_data_dir = find_file(global_config.PROJECT_PATH, '{}_filter_block.txt'.format(task), exclude_key='v1', recursive=True)
        pass_injections = [line.strip() + '$BYPASS_LABEL$1' for line in open(pass_data_dir, mode='r', encoding='utf8').readlines()]
        block_injections = [line.strip() + '$BYPASS_LABEL$0' for line in open(block_data_dir, mode='r', encoding='utf8').readlines()]
        sum_injections = pass_injections + block_injections
        if not os.path.exists('{}/classification_datasets/{}'.format(base_dir, task)):
            os.makedirs('{}/classification_datasets/{}'.format(base_dir, task))

    random.shuffle(sum_injections)

    test_set = sum_injections[:len(sum_injections) // 5]
    train_set = sum_injections[len(sum_injections) // 5:]

    fout_train = open('{}/classification_datasets/{}/{}_train.txt'.format(base_dir, task, task), mode='w', encoding='utf8')
    fout_test = open('{}/classification_datasets/{}/{}_test.txt'.format(base_dir, task, task), mode='w', encoding='utf8')

    for injection in train_set:
        fout_train.write(injection + '\n')

    for injection in test_set:
        fout_test.write(injection + '\n')

    print('Generation done for {}'.format(task))


class SimilarityCalculator:
    def __init__(self, task, num_topics=100):
        self.corpus = None
        self.dic = None
        self.contents = []

        self.contents = load_injections(task, itype='all')
        self.prepare_dic_corpus()

        self.lsi = models.LsiModel(self.corpus, id2word=self.dic, num_topics=num_topics)
        # self.index = similarities.Similarity('index', self.lsi[self.corpus], num_features=self.lsi.num_topics)
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])
        self.matched = set()

    def prepare_dic_corpus(self):
        texts = self.contents
        dic = corpora.Dictionary([content[1].split() for content in self.contents])
        corpus = [dic.doc2bow(text[1].split()) for text in texts]
        self.corpus = corpus
        self.dic = dic
        return dic, corpus

    def find_similar_pairs(self, query_injection):
        query_bow = self.dic.doc2bow(query_injection.lower().split())
        query_lsi = self.lsi[query_bow]
        sims = self.index[query_lsi]
        sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        # print('max similarity:{}'.format(sorted_sims[0][1]))
        # print('min similarity:{}'.format(sorted_sims[-1][1]))
        if sorted_sims[0][1] > 0:
            while len(sorted_sims) > 1 and self.contents[sorted_sims[0][0]][1] in self.matched:
                sorted_sims.remove(sorted_sims[0])
            self.matched.add(self.contents[sorted_sims[0][0]][1])
            return query_injection, self.contents[sorted_sims[0][0]][1]
        else:
            return '', ''


def __extract_translator_dataset__(source_task, target_task):
    sim_cal = SimilarityCalculator(source_task)
    query_injections = load_injections(target_task)

    dir_to_save = '{}/runtime_materials/translation_datasets/{}2{}'.format(global_config.PROJECT_PATH, source_task, target_task)

    # if os.path.getsize(dir_to_save) > 1000 and find_target_file(dir_to_save, '.txt'):
    #     print('Find processed translation dataset for {}2{}, return ...'.format(task1, task2))
    #     return

    if not os.path.exists(dir_to_save):
        os.makedirs(dir_to_save)

    source_lan_path = os.path.join(dir_to_save, '{}2{}_source.txt'.format(source_task, target_task))
    target_lan_path = os.path.join(dir_to_save, '{}2{}_target.txt'.format(source_task, target_task))

    source_injections = []
    target_injections = []

    for _, query in tqdm.tqdm(query_injections, postfix='extract similar injection_utils {} to {}'.format(source_task, target_task)):
        target_injection, source_injection = sim_cal.find_similar_pairs(query)
        if source_injection and target_injection:
            source_injections.append(source_injection)
            target_injections.append(target_injection)

    source_injections_set = set(source_injections)
    target_injections_set = set(target_injections)

    f_src_out = open(source_lan_path, mode='w', encoding='utf8')
    f_tgt_out = open(target_lan_path, mode='w', encoding='utf8')
    for source_injection, target_injection in zip(source_injections, target_injections):
        # if target_injection not in target_injections_set:
        f_src_out.write(source_injection + '\n')
        f_tgt_out.write(target_injection + '\n')
    print('source_injections{}'.format(len(source_injections_set)))
    print('target_injections{}'.format(len(target_injections_set)))

    return source_injections, target_injections


def __prepare_translation_dataset__(task1, task2):
    source_raw_data_path = find_file(global_config.PROJECT_PATH, '{}2{}_source.txt'.format(task1, task2))
    target_raw_data_path = find_file(global_config.PROJECT_PATH, '{}2{}_target.txt'.format(task1, task2))
    source_raw_data = open(source_raw_data_path, mode='r').readlines()
    target_raw_data = open(target_raw_data_path, mode='r').readlines()

    train_source_path = source_raw_data_path.replace(os.path.basename(source_raw_data_path), 'src-train.txt')
    train_target_path = target_raw_data_path.replace(os.path.basename(target_raw_data_path), 'tgt-train.txt')

    test_source_path = source_raw_data_path.replace(os.path.basename(source_raw_data_path), 'src-val.txt')
    test_target_path = target_raw_data_path.replace(os.path.basename(target_raw_data_path), 'tgt-val.txt')

    f_train_source = open(train_source_path, mode='w', encoding='utf8')
    f_train_target = open(train_target_path, mode='w', encoding='utf8')

    f_test_source = open(test_source_path, mode='w', encoding='utf8')
    f_test_target = open(test_target_path, mode='w', encoding='utf8')

    for i, (s, t) in enumerate(zip(source_raw_data, target_raw_data)):
        if i + 1 < len(source_raw_data) * 0.8:
            f_train_source.write(s + '\n')
            f_train_target.write(t + '\n')
        else:
            f_test_source.write(s + '\n')
            f_test_target.write(t + '\n')


def extract_translator_dataset(task1, task2):
    __extract_translator_dataset__(task1, task2)
    __prepare_translation_dataset__(task1, task2)

    __extract_translator_dataset__(task2, task1)
    __prepare_translation_dataset__(task2, task1)


def load_injections(task, itype='pass'):
    fname = '{}_pass.txt'.format(task) if itype == 'pass' else '{}.txt'.format(task)
    data_dir = find_file(global_config.PROJECT_PATH, 'injection_cases/{}/{}'.format(task, fname))
    fin = open(data_dir, mode='r', encoding='utf8')

    contents = []
    for i, line in enumerate(fin.readlines()):
        contents.append((i, line.split('$BYPASS_LABEL$')[0].strip()))
    fin.close()
    return contents


def prepare_word2vec(workers=1):
    word2vec_path = '{}/word2vec'.format(global_config.PROJECT_PATH)
    if not find_file(word2vec_path, 'w2v.txt', recursive=True):
        train_word2vec(workers)


def prepare_injection_cases(tasks, multi_process=False):
    for t in tasks:
        if multi_process:
            p = multiprocessing.Process(target=generate_injection_cases, args=(t,))
            p.start()
            p.join()
        else:
            generate_injection_cases(t)


def prepare_classification_datasets(tasks, multi_process=False):
    for t in tasks:
        if multi_process:
            multiprocessing.Process(target=__prepare_classification_dataset__, args=(t,)).start()

        else:
            __prepare_classification_dataset__(t)


def __prepare_classification_dataset__(t):
    generate_classification_dataset(t)
    print('Classification dataset generated for {}'.format(t))


def prepare_classifier_models(tasks, multi_process=False):
    for t in tasks:
        if multi_process:

            p = multiprocessing.Process(target=train_classifier_by_task, args=(t,))
            p.start()
            p.join()
            time.sleep(30)
        else:
            train_classifier_by_task(t)


def prepare_translation_datasets(tasks, multi_process=False):
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            if multi_process:
                multiprocessing.Process(target=extract_translator_dataset, args=(tasks[i], tasks[j])).start()
            else:
                extract_translator_dataset(tasks[i], tasks[j])


def prepare_runtime_materials(force_reprepare=False):
    '''
    'force_reprepare'  clean the unfinished preprocessing trash if any
    '''
    # clean the unfinished preprocessing if any
    if force_reprepare:
        runtime_materials_path = os.path.join(global_config.PROJECT_PATH, 'runtime_materials')
        if os.path.exists(runtime_materials_path):
            shutil.rmtree(runtime_materials_path)

    # To simplify and make it easier to run,
    # I group all the preparations by multiprocessing behind run main experiment
    # Note the preprocessing are in the specific order, no not change,
    # Some steps could be skipped given the processed data is attached with the code

    # injection_tasks = ["sqli", "xss", "osi", "phpi", "xmli", "htmli"]
    injection_tasks = ["sqli"]
    # injection_tasks = ["xss"]
    # injection_tasks = ["osi"]
    # injection_tasks = ["phpi"]
    # injection_tasks = ["xmli"]
    # injection_tasks = ["htmli"]

    multi_processing = False
    injection_bypass_check(injection_tasks, multi_processing)
    # prepare_classification_datasets(injection_tasks, multi_processing)  # this function contains the up-line function
    # prepare_word2vec(os.cpu_count())
    # prepare_classifier_models(injection_tasks, multi_process=False)
    # prepare_translation_datasets(injection_tasks, multi_processing)
    # prepare_translator_models(injection_tasks, multi_processing=False)


if __name__ == '__main__':
    prepare_runtime_materials()
